# ACG Project 技术实现总结

## 1. 核心渲染架构与采样算法

### 路径追踪与渲染方程 (Path Tracing)
本项目基于物理的路径追踪算法，核心是求解如下形式的渲染方程：
$$L_o(p, \omega_o) = L_e(p, \omega_o) + \int_{\Omega} f_r(p, \omega_i, \omega_o) L_i(p, \omega_i) \cos\theta_i d\omega_i$$
其中：
- $L_e$ 为表面的自发光项。
- $f_r$ 为双向反射分布函数 (BRDF)。
- $\cos\theta_i$ 是入射光与表面法线的夹角余弦，对应 HLSL 中的 `dot(N, L)`。

**核心迭代逻辑：**
```hlsl
float3 radiance = 0;    // 累积贡献
float3 throughput = 1;  // 路径衰减权重

for (int bounce = 0; bounce < maxBounces; bounce++) {
    // 1. 寻找最近交点
    HitRecord hit = TraceRay(ray);
    if (!hit.isIntersected) {
        radiance += throughput * SampleEnvironment(ray.dir);
        break;
    }

    // 2. 处理自发光
    radiance += throughput * hit.material.emission;

    // 3. 重要性采样与 Russian Roulette (RR)
    // 根据材质属性采样下一个方向，并获取该方向的概率密度函数 (PDF)
    float3 nextDir;
    float pdf;
    float3 f = SampleBSDF(hit, -ray.dir, nextDir, pdf);
    
    // 更新权重：throughput *= (f * cos) / pdf
    throughput *= f * saturate(dot(hit.normal, nextDir)) / pdf;

    // 4. 轮盘赌 (Russian Roulette) 终止判据
    // 当路径能量过低时，以一定概率平等的终止路径，防止无限迭代
    float rrProb = min(max(throughput.r, max(throughput.g, throughput.b)), 0.95f);
    if (bounce > 3) {
        if (Random() > rrProb) break;
        throughput /= rrProb; // 能量补偿
    }

    ray = CreateRay(hit.pos, nextDir);
}
```

### 多重重要性采样 (MIS)
为了同时兼顾大光源采样和材质高光采样，项目采用了多重重要性采样。使用 **Power Heuristic** ($\beta=2$) 来加权：
$$w(p_i) = \frac{p_i(x)^\beta}{\sum_j p_j(x)^\beta}$$
在渲染中体现为：
1. **光源采样权重**：$w_{light} = \frac{PDF_{light}^2}{PDF_{light}^2 + PDF_{bsdf}^2}$
2. **BSDF 采样权重**：$w_{bsdf} = \frac{PDF_{bsdf}^2}{PDF_{bsdf}^2 + PDF_{light}^2}$

## 2. 材质系统 (Material System)

### Principled BSDF (Disney) 模型
项目实现了一个基于 Disney Principled 框架的材质系统，综合了漫反射与镜面反射项。

- **法线分布函数 (NDF)**：基于 Trowbridge-Reitz GGX，描述微平面的粗糙程度分布。
  $$D(H) = \frac{\alpha^2}{\pi ((N \cdot H)^2 (\alpha^2 - 1) + 1)^2}$$
  其中 $H$ 为半角向量，$\alpha = roughness^2$。

- **几何遮蔽项 (Geometry)**：采用 Smith 模型，结合 Schlick-GGX 近似，处理微表面间的自遮挡。
  $$G(V, L) = G_1(V) G_1(L)$$
  $$G_1(v) = \frac{N \cdot v}{(N \cdot v)(1 - k) + k}$$
  对于直接光路径计算，重映射系数 $k_{direct} = \frac{(\alpha+1)^2}{8}$；对于阴影/光流计算使用 $k_{IBL} = \frac{\alpha}{2}$。

- **菲涅尔项 (Fresnel)**：Schlick 近似公式。
  $$F(\theta) = F_0 + (1 - F_0)(1 - \cos\theta)^5$$
  其中 $F_0$ 为垂直反射率。

### 多层材质逻辑 (Layered Materials)
本系统支持多层扩展（如涂层 Clearcoat、光泽 Sheen、次表面散射 SSS）。通过解析内存布局中的 `ExtendedData` 位标志来决定层级逻辑。

**层叠加逻辑伪代码：**
```hlsl
// 利用随机数在不同层之间进行概率选择或能量混合
if (hasExtendedLayers) {
    if (TryLayer(LAYER_CLEARCOAT)) {
        // 计算涂层反射（通常为高折射率、低粗糙度的白色高光层）
        float3 f_coat = EvaluateClearcoat(hit, V, L);
        float pdf_coat = PdfClearcoat(hit, V, L);
        return (f_coat * weight) / pdf_coat;
    }
}

// 基础层计算
float3 f_base = EvaluatePrincipledBSDF(hit, V, L);
// 如果有 Sheen 层，则在漫反射上叠加边缘光
if (flags & LAYER_SHEEN) {
    f_base += EvaluateSheen(hit, V, L);
}
// 如果有 SSS 层，则根据混合系数在漫反射与次表面之间插值
if (flags & LAYER_SSS) {
    f_base = lerp(f_base, EvaluateSSS(hit, V, L), subsurfaceFactor);
}
```

- **各向异性分布**：针对拉丝金属等材质，使用各向异性的 GGX NDF。
  $$D_{aniso}(H) = \frac{1}{\pi \alpha_x \alpha_y \left( \frac{(H \cdot T)^2}{\alpha_x^2} + \frac{(H \cdot B)^2}{\alpha_y^2} + (H \cdot N)^2 \right)^2}$$
  其中 $T, B$ 分别为切线和副切线向量。

## 3. 光学特效与纹理系统

### 景深 (Depth of Field)
本项目实现了物理驱动的薄透镜（Thin Lens）模拟，相较于理想小孔模型，能产生平滑的焦外虚化效果。
1. **对焦平面计算**：首先计算从小孔中心射出的光线在对焦距离 $d_{focus}$ 处的交点 $P_{focal}$。
   $$P_{focal} = P_{eye} + \omega_{pinhole} \cdot d_{focus}$$
2. **孔径随机采样**：在半径为 $R_{aperture}$ 的镜头圆盘内进行随机采样（本项目采用圆盘采样 `SampleDisk`），得到光线的实际发射起点 $P_{lens}$。
   $$P_{lens} = P_{eye} + \xi_x \cdot \vec{Right} + \xi_y \cdot \vec{Up}, \quad \text{其中} \sqrt{\xi_x^2 + \xi_y^2} \le R_{aperture}$$
3. **方向重定向**：将采样点 $P_{lens}$ 指向焦点 $P_{focal}$ 得到最终光线方向。
   $$\omega_{new} = \text{Normalize}(P_{focal} - P_{lens})$$

### 抗锯齿 (Anti-aliasing)
项目采用了时间轴上的亚像素抖动算法（Sub-pixel Jittering）来实现超采样抗锯齿：
1. **抖动采样**：在每一帧渲染时，对光线穿过像素中心的坐标添加 $[-0.5, 0.5]$ 的随机偏移。
   $$Coord_{jitter} = Pixel_{index} + 0.5 + (\zeta - 0.5), \quad \zeta \sim U(0, 1)^2$$
2. **多帧累积**：利用累积缓冲区（Accumulation Buffer）对连续多帧的结果进行加权平均。
   $$Color_{final} = \frac{1}{N} \sum_{i=1}^{N} Color_i$$
这种方法在不显著增加单帧计算开销的前提下，通过时间换取空间的方式有效消除了边缘锯齿。

### 色散 (Chromatic Dispersion)
色散模拟了折射率随频率（波长）变化的物理特性。项目采用了基于通道分离的蒙特卡洛采样法：
- **随机波长选择**：对于路径追踪中的每一次折射，以等概率随机选取 R、G、B 通道之一作为当前采样的响应波长。
- **折射率偏移模型**：
  - $n_{red} = n_{base} \cdot (1 - S_{disp})$
  - $n_{green} = n_{base}$
  - $n_{blue} = n_{base} \cdot (1 + S_{disp})$
  其中 $S_{disp}$ 是色散强度系数。
- **能量补偿**：为了保证结果无偏，采样的路径权重需要乘以 3（代表三分之一的采样概率）：
  `throughput.rgb *= (choice == RED ? float3(3,0,0) : ...)`
通过多帧累积，不同折射率产生的路径偏转会自然形成光谱色散效果。

### 虚拟纹理 (Virtual Texture)
针对海量高精度纹理导致的显存瓶颈，项目实现了一套 Tile-based 间接映射系统：
1. **分块结构**：将大图拆分为 $256 \times 256$ 的 Tile，物理显存（Physical Pool）仅按需存储被访问到的 Tile 数据。
2. **逻辑寻址步骤**：
   - **Page 查找**：根据虚拟 UV 定位二级查找表（Indirection Table）中的页索引。
   - **坐标转换**：从 Indirection Table 获取该页在物理池中的位置，并结合切片内偏移量计算最终采样 UV。
   $$UV_{phys} = \frac{TilePos(ID) \cdot 256 + (UV_{virt} \cdot Size) \pmod{256}}{PoolSize}$$
3. **按需加载 (Demand Loading)**：在渲染循环中实时检测缺失的 Tile 索引，并动态从磁盘上传至 GPU。

### 卡通化后处理 (Cartoon Post-processing)
项目在输出后期集成了基于图像空间的艺术化滤镜：
1. **色彩量化 (Posterization)**：通过减少色彩分量的连续性，产生独特的色块效果。
   $$C_{step} = \frac{255}{\text{Levels}}, \quad C_{out} = \lfloor \frac{C_{in}}{C_{step}} \rfloor \cdot C_{step}$$
2. **Sobel 边缘检测**：使用 $3 \times 3$ 卷积核检测亮度梯度变化。
   - **算子**：$K_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}, \quad K_y = \begin{bmatrix} 1 & 2 & 1 \\ 0 & 0 & 0 \\ -1 & -2 & -1 \end{bmatrix}$
   - **梯度幅值**：$G = \sqrt{G_x^2 + G_y^2}$
   - **描边逻辑**：当梯度 $G$ 超过预设阈值时，显著降低颜色明度，从而在物体边缘生成对比明显的描边线条。

---

