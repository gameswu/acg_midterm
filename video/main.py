from manimlib import *
import numpy as np

class RelativisticRayTracing(Scene):
    def construct(self):
        # Part 1: Introduction - The Physics of Ray Tracing
        self.intro_ray_tracing()
        
        # Part 2: Theory - Special Relativity in Rendering
        self.theory_section()
        
        # Part 3: Results Showcase
        self.results_showcase()

    def intro_ray_tracing(self):
        # Title - PERSISTENT
        title = Text("Part 1: The Physics of Ray Tracing", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 1.1 The Concept of Reverse Ray Tracing
        # Center the diagram initially
        camera = Square(side_length=0.5).set_fill(BLUE, opacity=0.5).move_to(LEFT * 4)
        camera_label = Text("Camera", font_size=24).next_to(camera, DOWN)
        
        screen = Line(UP * 1.5, DOWN * 1.5).move_to(LEFT * 2)
        screen_label = Text("Image Plane", font_size=24).next_to(screen, UP)
        
        sphere = Circle(radius=1).set_fill(RED, opacity=0.5).move_to(RIGHT * 2)
        sphere_label = Text("Object", font_size=24).next_to(sphere, DOWN)
        
        light = Circle(radius=0.2, color=YELLOW, fill_opacity=1).move_to(RIGHT * 4 + UP * 2)
        light_label = Text("Light", font_size=24).next_to(light, RIGHT)

        scene_group = VGroup(camera, camera_label, screen, screen_label, sphere, sphere_label, light, light_label)
        self.play(FadeIn(scene_group))

        # 1.2 Shooting Rays
        ray_start = camera.get_center()
        pixel_point = screen.get_center()
        hit_point = sphere.get_left()
        
        ray_segment1 = Line(ray_start, pixel_point, color=WHITE)
        ray_segment2 = Line(pixel_point, hit_point, color=WHITE)
        
        self.play(ShowCreation(ray_segment1), run_time=0.5)
        self.play(ShowCreation(ray_segment2), run_time=1.0)
        
        # Intersection
        flash = Flash(hit_point, color=WHITE, flash_radius=0.2)
        self.play(flash)
        
        # Shadow Ray
        shadow_ray = Line(hit_point, light.get_center(), color=YELLOW)
        self.play(ShowCreation(shadow_ray), run_time=0.5)

        # Annotate: Label key terms on diagram
        label_Lo = Tex(r"L_o", color=BLUE, font_size=28).next_to(ray_segment2, UP, buff=0.1)
        label_Li = Tex(r"L_i", color=YELLOW, font_size=28).next_to(shadow_ray, UP, buff=0.1)
        label_n = Tex(r"n", color=GREEN, font_size=28).next_to(sphere, RIGHT, buff=0.1).shift(LEFT*0.5+UP*0.5)
        
        self.play(Write(label_Lo), Write(label_Li), Write(label_n))
        self.wait(2)

        # 1.3 CLEANUP DIAGRAM BEFORE EQUATION
        # "To understand the math, let's look at the rendering equation."
        self.play(
            FadeOut(scene_group), FadeOut(ray_segment1), FadeOut(ray_segment2), FadeOut(shadow_ray),
            FadeOut(label_Lo), FadeOut(label_Li), FadeOut(label_n)
        )
        
        # 1.4 The Classical Rendering Equation
        eq_title = Text("The Classical Rendering Equation", font_size=40, color=BLUE).to_edge(UP, buff=1.5)
        rendering_eq = Tex(
            r"L_o(p, \omega_o) = L_e(p, \omega_o) + \int_{\Omega} f_r(p, \omega_i, \omega_o) L_i(p, \omega_i) (\omega_i \cdot n) d\omega_i"
        ).scale(0.8).next_to(eq_title, DOWN, buff=0.5)
        
        self.play(Write(eq_title), Write(rendering_eq))
        self.wait(1)

        # 1.5 The Assumption of Infinite Speed
        assumption_eq = Tex(r"c = \infty \Rightarrow \Delta t = 0", font_size=36, color=GREY)
        assumption_eq.next_to(rendering_eq, DOWN, buff=0.8)
        
        text_assumption = Text("Light arrives instantly.", font_size=32, color=GREY).next_to(assumption_eq, DOWN)
        
        self.play(Write(assumption_eq), Write(text_assumption))
        self.wait(2)
        
        # 1.6 Transition to Relativistic
        # Clear everything for the new concept
        self.play(
            FadeOut(eq_title), FadeOut(rendering_eq), FadeOut(assumption_eq), FadeOut(text_assumption)
        )
        
        # What if c is finite?
        question = Text("But what if c is finite?", font_size=48, color=RED).move_to(UP * 0.5)
        self.play(Write(question))
        self.wait(1)
        
        modified_eq = Tex(
            r"L_o(p, \omega_o, t) = L_e(p, \omega_o) + \int_{\Omega} f_r(p, \omega_i, \omega_o, \mathbf{v}) \times",
            r"L_i(p, \omega_i, t - \frac{d}{c}) \cdot (\omega_i \cdot n) \, d\omega_i",
            font_size=32, color=ORANGE
        ).next_to(question, DOWN, buff=1.0)
        
        explanation = Text("Time Delay & Velocity Dependence", font_size=32, color=ORANGE).next_to(modified_eq, DOWN)
        
        self.play(Write(modified_eq))
        self.play(Write(explanation))
        self.wait(3)
        
        # Cleanup for next part
        self.play(
            FadeOut(question), FadeOut(modified_eq), FadeOut(explanation),
            FadeOut(title)
        )

    def theory_section(self):
        title = Text("Part 2: Relativistic Effects in Rendering", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Section Header
        header = Text("1. Special Relativity Basis", font_size=36, color=BLUE).next_to(title, DOWN)
        self.play(Write(header))

        # Lorentz Transform Matrix
        matrix_eq = Tex(
            r"\begin{bmatrix} ct' \\ x' \end{bmatrix} = "
            r"\begin{bmatrix} \gamma & -\beta\gamma \\ -\beta\gamma & \gamma \end{bmatrix}"
            r"\begin{bmatrix} ct \\ x \end{bmatrix}"
        )
        self.play(Write(matrix_eq))
        self.wait(2)
        self.play(FadeOut(matrix_eq), FadeOut(header))

        # Aberration
        self.derive_aberration(title)
        
        # Doppler
        self.derive_doppler(title)

        # Headlight
        self.derive_headlight(title)
        
        # CG Implementation
        self.derive_cg_implementation(title)
        
        # Cleanup
        self.play(FadeOut(title))

    def derive_headlight(self, title_obj):
        subtitle = Text("4. Headlight Effect", font_size=36, color=YELLOW).next_to(title_obj, DOWN)
        self.play(Write(subtitle))
        
        # Visual: Cone narrowing
        # Left side
        cone_wide = AnnularSector(outer_radius=3, inner_radius=0, angle=PI/3, color=YELLOW, fill_opacity=0.3).rotate(0).move_to(LEFT * 3)
        cone_narrow = AnnularSector(outer_radius=4, inner_radius=0, angle=PI/6, color=YELLOW, fill_opacity=0.6).rotate(0).move_to(LEFT * 3)
        
        cone_label = Text("Field of View", font_size=24).next_to(cone_wide, DOWN)
        
        self.play(ShowCreation(cone_wide), Write(cone_label))
        self.play(Transform(cone_wide, cone_narrow))
        
        # Formula
        # Right side
        intensity_formula = Tex(r"I' = I \cdot D^2", font_size=48).move_to(RIGHT * 2)
        note = Text("(n=2 for balance)", font_size=24, color=GREY).next_to(intensity_formula, DOWN)
        
        self.play(Write(intensity_formula), Write(note))
        self.wait(2)
        
        self.play(FadeOut(cone_wide), FadeOut(cone_label), FadeOut(intensity_formula), FadeOut(note), FadeOut(subtitle))

    def derive_cg_implementation(self, title_obj):
        subtitle = Text("5. Algorithm Implementation", font_size=36, color=GREEN).next_to(title_obj, DOWN)
        self.play(Write(subtitle))
        
        # Layout: Left (Code), Right (Visual Animation)
        
        # --- Left: Code Block ---
        # Make it narrower and move to far left
        code_bg = Rectangle(width=5.5, height=6.5, fill_color=BLACK, fill_opacity=0.8, stroke_color=WHITE).to_edge(LEFT, buff=0.2)
        code_header = Text("Shader Implementation", font_size=24).next_to(code_bg, UP)
        
        # Updated to match PPT logic exactly
        code_str = (
            "// 1. Aberration\n"
            "vec3 v_hat = v / beta;\n"
            "float cos_t_p = dot(dir, v_hat);\n"
            "float cos_t = (cos_t_p - beta) / \n"
            "              (1.0 - beta * cos_t_p);\n"
            "vec3 newDir = reconstruct(v_hat, cos_t);\n\n"
            "// 2. Doppler\n"
            "vec3 lightDir = -newDir;\n"
            "float cos_t_d = dot(lightDir, v_hat);\n"
            "float D = gamma * (1.0 + beta * cos_t_d);\n\n"
            "// 3. Headlight & Shift\n"
            "float hFactor = clamp(pow(D, 2.0), 0.1, 10.0);\n"
            "vec3 color = sample(newDir, D) * hFactor;"
        )
        
        code_text = Text(code_str, font="Monospace", font_size=14, t2c={"beta": YELLOW, "gamma": YELLOW, "D": RED}).move_to(code_bg)
        code_text.align_to(code_bg, UL).shift(RIGHT*0.2 + DOWN*0.2)
        
        self.play(FadeIn(code_bg), Write(code_header), Write(code_text))
        
        # --- Right: Visual Animation ---
        # Setup mini scene on the right half
        right_center = RIGHT * 3.0
        
        # Camera
        cam_dot = Dot(point=right_center + LEFT*2 + DOWN*2, color=BLUE)
        cam_label = Text("Cam", font_size=16).next_to(cam_dot, DOWN)
        
        # Velocity Vector
        vel_arrow = Arrow(cam_dot.get_center(), cam_dot.get_center() + RIGHT*1.5, color=YELLOW, buff=0)
        vel_label = Text("v", font_size=16, color=YELLOW).next_to(vel_arrow, UP)
        
        # Object (Star/Sphere)
        obj = Circle(radius=0.5, color=WHITE, fill_opacity=0.5).move_to(right_center + RIGHT*1 + UP*2)
        
        visual_group = VGroup(cam_dot, cam_label, vel_arrow, vel_label, obj)
        self.play(FadeIn(visual_group))
        
        # --- Animation Sequence Synchronized with Code ---
        
        # 1. Aberration Logic
        # Show original ray direction (dir)
        orig_ray = Arrow(cam_dot.get_center(), cam_dot.get_center() + UP*3 + RIGHT*1, color=GREY, buff=0)
        orig_label = Text("dir", font_size=14).next_to(orig_ray.get_end(), UP)
        self.play(ShowCreation(orig_ray), Write(orig_label))
        
        # Show v_hat (direction of motion)
        # Already shown as v, but emphasize
        self.play(vel_arrow.animate.scale(1.2).set_color(ORANGE))
        self.play(vel_arrow.animate.scale(1/1.2).set_color(YELLOW))
        
        # Show newDir (bent ray towards object)
        new_ray = Arrow(cam_dot.get_center(), obj.get_center(), color=BLUE, buff=0)
        new_label = Text("newDir", font_size=14, color=BLUE).next_to(new_ray.get_end(), LEFT)
        self.play(TransformFromCopy(orig_ray, new_ray), Write(new_label))
        
        # 2. Doppler Logic
        # Show lightDir = -newDir (Ray from object to camera)
        light_ray = Arrow(obj.get_center(), cam_dot.get_center(), color=RED, buff=0)
        light_label = Text("lightDir", font_size=14, color=RED).next_to(light_ray.get_start(), DOWN)
        self.play(ShowCreation(light_ray), Write(light_label))
        
        # Show angle calculation (dot product visual)
        angle_arc = Arc(radius=0.5, start_angle=light_ray.get_angle(), angle=vel_arrow.get_angle() - light_ray.get_angle(), arc_center=cam_dot.get_center(), color=GREEN)
        self.play(ShowCreation(angle_arc))
        
        # 3. Headlight & Shift
        # Show D factor effect
        d_val = Text("D > 1.0", font_size=24, color=RED).next_to(obj, RIGHT)
        self.play(Write(d_val))
        
        # Brightness (Headlight)
        self.play(obj.animate.set_fill(WHITE, opacity=1.0).scale(1.2))
        
        # Color Shift (Blue shift)
        self.play(obj.animate.set_color(BLUE).set_fill(BLUE))
        
        self.wait(3)
        
        self.play(
            FadeOut(code_bg), FadeOut(code_header), FadeOut(code_text),
            FadeOut(visual_group), FadeOut(orig_ray), FadeOut(orig_label), 
            FadeOut(new_ray), FadeOut(new_label),
            FadeOut(light_ray), FadeOut(light_label), FadeOut(angle_arc), FadeOut(d_val),
            FadeOut(subtitle)
        )

    def derive_aberration(self, title_obj):
        subtitle = Text("2. Relativistic Aberration", font_size=36, color=BLUE).next_to(title_obj, DOWN)
        self.play(Write(subtitle))
        
        # Layout: Left (Visual), Right (Math)
        
        # --- Visual: The "Searchlight" Effect ---
        # A circle of vectors representing light rays emitted/received
        circle_radius = 2.0
        circle_center = LEFT * 3 + DOWN * 0.5
        
        # Create arrows
        arrows = VGroup()
        num_arrows = 12
        for i in range(num_arrows):
            angle = i * (2 * PI / num_arrows)
            # Arrow pointing OUT from center
            end_point = circle_center + np.array([np.cos(angle), np.sin(angle), 0]) * circle_radius
            arrow = Arrow(circle_center, end_point, buff=0, color=WHITE)
            arrows.add(arrow)
            
        label_visual = Text("Field of View Directions", font_size=24).next_to(arrows, DOWN)
        
        self.play(ShowCreation(arrows), Write(label_visual))
        
        # --- Math: Step-by-Step Derivation ---
        # Using aligned equations
        math_content = Tex(
            r"\text{Velocity Addition: } & u'_x = \frac{u_x - v}{1 - u_x v / c^2} \\"
            r"\text{Substitution: } & u_x = c \cos \theta \\"
            r"\text{Result: } & \cos \theta' = \frac{\cos \theta - \beta}{1 - \beta \cos \theta}",
            tex_to_color_map={r"\beta": YELLOW, r"\theta": BLUE, r"\theta'": RED}
        ).scale(0.7).to_edge(RIGHT, buff=1)
        
        self.play(Write(math_content[0])) # Velocity Addition
        self.wait(1)
        self.play(Write(math_content[1])) # Substitution
        self.wait(1)
        self.play(Write(math_content[2])) # Result
        
        # --- Animation: Apply Beta ---
        beta_tracker = ValueTracker(0.0)
        
        def update_arrows(mob):
            b = beta_tracker.get_value()
            new_arrows = VGroup()
            for i in range(num_arrows):
                angle = i * (2 * PI / num_arrows)
                cos_t = np.cos(angle)
                sin_t = np.sin(angle)
                
                # Aberration Formula (Observer moving)
                # Rays bunch up in direction of motion
                denom = 1.0 - b * cos_t
                if denom == 0: denom = 0.001
                
                cos_prime = (cos_t - b) / denom
                sin_prime = sin_t * np.sqrt(1 - b**2) / denom
                
                angle_prime = np.arctan2(sin_prime, cos_prime)
                
                # Color shift based on angle (Doppler hint)
                # Head on (0) -> Blue, Back (PI) -> Red
                color = interpolate_color(BLUE, RED, angle_prime / PI)
                
                end_point = circle_center + np.array([np.cos(angle_prime), np.sin(angle_prime), 0]) * circle_radius
                arrow = Arrow(circle_center, end_point, buff=0, color=color)
                new_arrows.add(arrow)
            mob.become(new_arrows)
            
        arrows.add_updater(update_arrows)
        
        # Animate Beta 0 -> 0.8
        beta_text = Text("Beta: 0.00", font_size=24).next_to(label_visual, DOWN)
        beta_text.add_updater(lambda m: m.become(Text(f"Beta: {beta_tracker.get_value():.2f}", font_size=24).next_to(label_visual, DOWN)))
        
        self.play(FadeIn(beta_text))
        self.play(beta_tracker.animate.set_value(0.8), run_time=4)
        self.wait(1)
        
        arrows.remove_updater(update_arrows)
        self.play(FadeOut(arrows), FadeOut(label_visual), FadeOut(math_content), FadeOut(beta_text), FadeOut(subtitle))

    def derive_doppler(self, title_obj):
        subtitle = Text("3. Doppler Shift", font_size=36, color=RED).next_to(title_obj, DOWN)
        self.play(Write(subtitle))
        
        # --- Concept: Phase Invariance ---
        concept_text = Text("Key Idea: Phase (Wave Count) is Invariant", font_size=32, color=BLUE).next_to(subtitle, DOWN, buff=0.5)
        self.play(Write(concept_text))
        
        # --- Visual: Wavefronts (Up in Scene) ---
        # Draw a source emitting waves (Shifted UP)
        source_pos = LEFT * 3 + UP * 1
        source_dot = Dot(source_pos, color=YELLOW)
        source_label = Text("Source", font_size=20).next_to(source_dot, UP)
        
        waves = VGroup()
        # Use Green/Yellow-Green for neutral source
        neutral_color = GREEN
        for i in range(1, 8):
            waves.add(Circle(radius=i*0.5, color=neutral_color, stroke_opacity=0.5).move_to(source_pos))
            
        scene_visual = VGroup(source_dot, source_label, waves)
        self.play(FadeIn(scene_visual))
        
        # Observer (Shifted UP)
        obs_dot = Dot(source_pos + RIGHT*4, color=BLUE)
        obs_label = Text("Observer", font_size=20, color=BLUE).next_to(obs_dot, UP)
        
        self.play(FadeIn(obs_dot), FadeIn(obs_label))
        
        # --- Signal Plot (Bottom of Scene) ---
        # Show what the observer "sees" or "measures"
        
        # Axes for signal
        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[-1.5, 1.5, 1],
            width=6, height=2,
            axis_config={"include_tip": False, "include_ticks": False, "color": GREY}
        ).to_edge(BOTTOM).shift(UP * 0.5)
        
        axes_label = Text("Observed Signal (Frequency Shift)", font_size=24, color=WHITE).next_to(axes, UP)
        
        # Use ValueTracker for smooth update of frequency
        freq_tracker = ValueTracker(1.0)
        
        # Graph that updates based on tracker
        signal_curve = axes.get_graph(lambda t: np.sin(freq_tracker.get_value() * t), color=neutral_color, x_range=[0, 12])
        
        def update_curve(mob):
            f = freq_tracker.get_value()
            # Transition color from Neutral (Green) to Blue
            # Map f=1.0 -> Green, f=3.0 -> Blue
            alpha = (f - 1.0) / 2.0
            new_color = interpolate_color(neutral_color, BLUE, alpha)
            
            mob.become(
                axes.get_graph(lambda t: np.sin(f * t), color=new_color, x_range=[0, 12])
            )

        signal_curve.add_updater(update_curve)
        
        self.play(FadeIn(axes), FadeIn(axes_label), ShowCreation(signal_curve))
        
        # --- Animation: Moving Observer ---
        velocity_arrow = Arrow(obs_dot.get_center(), obs_dot.get_center() + LEFT, color=BLUE)
        self.play(ShowCreation(velocity_arrow))
        
        # Text explanation (Situated between scene and graph)
        eq_text = Tex(r"\omega' > \omega", color=BLUE).move_to(LEFT * 3 + DOWN * 1.5)
        self.play(Write(eq_text))
        
        # Move Observer & Compress Wave
        self.play(
            obs_dot.animate.shift(LEFT * 2.5),
            freq_tracker.animate.set_value(3.0),
            run_time=4,
            rate_func=linear
        )
        
        signal_curve.remove_updater(update_curve)
        
        blueshift_text = Text("Blue Shift detected", font_size=24, color=BLUE).next_to(obs_dot, DOWN)
        self.play(Write(blueshift_text))
        self.wait(2)

        self.play(
            FadeOut(scene_visual), FadeOut(obs_dot), FadeOut(obs_label), FadeOut(velocity_arrow),
            FadeOut(axes), FadeOut(axes_label), FadeOut(signal_curve),
            FadeOut(concept_text), FadeOut(eq_text), FadeOut(blueshift_text), FadeOut(subtitle)
        )

    def derive_headlight(self, title_obj):
        subtitle = Text("4. Headlight Effect", font_size=36, color=YELLOW).next_to(title_obj, DOWN)
        self.play(Write(subtitle))
        
        # Visual: Cone narrowing
        # Left side
        cone_wide = AnnularSector(outer_radius=3, inner_radius=0, angle=PI/3, color=YELLOW, fill_opacity=0.3).rotate(0).move_to(LEFT * 3)
        cone_narrow = AnnularSector(outer_radius=4, inner_radius=0, angle=PI/6, color=YELLOW, fill_opacity=0.6).rotate(0).move_to(LEFT * 3)
        
        cone_label = Text("Field of View", font_size=24).next_to(cone_wide, DOWN)
        
        self.play(ShowCreation(cone_wide), Write(cone_label))
        self.play(Transform(cone_wide, cone_narrow))
        
        # Formula
        # Right side
        intensity_formula = Tex(r"I' = I \cdot D^2", font_size=48).move_to(RIGHT * 2)
        note = Text("(n=2 for balance)", font_size=24, color=GREY).next_to(intensity_formula, DOWN)
        
        self.play(Write(intensity_formula), Write(note))
        self.wait(2)
        
        self.play(FadeOut(cone_wide), FadeOut(cone_label), FadeOut(intensity_formula), FadeOut(note), FadeOut(subtitle))

    def derive_cg_implementation(self, title_obj):
        subtitle = Text("5. Algorithm Implementation", font_size=36, color=GREEN).next_to(title_obj, DOWN)
        self.play(Write(subtitle))
        
        # --- UI: macOS Code Window ---
        window_width = 6.0
        window_height = 5.5
        
        # Window Frame
        window_frame = RoundedRectangle(corner_radius=0.2, width=window_width, height=window_height, 
                                        fill_color=BLACK, fill_opacity=0.9, stroke_color=GREY, stroke_width=2)
        window_frame.to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
        
        # Title Bar (Aligned to Top and Left of Frame)
        title_bar = Rectangle(width=window_width, height=0.4, fill_color=GREY_D, fill_opacity=1, stroke_opacity=0)
        title_bar.align_to(window_frame, UP)
        title_bar.align_to(window_frame, LEFT)
        
        # Buttons
        red_dot = Dot(radius=0.12, color=RED, fill_opacity=1).move_to(title_bar.get_left() + RIGHT*0.3)
        yellow_dot = Dot(radius=0.12, color=YELLOW, fill_opacity=1).next_to(red_dot, RIGHT, buff=0.15)
        green_dot = Dot(radius=0.12, color=GREEN, fill_opacity=1).next_to(yellow_dot, RIGHT, buff=0.15)
        
        buttons = VGroup(red_dot, yellow_dot, green_dot)
        buttons.align_to(title_bar, LEFT).shift(RIGHT*0.2) 
        
        window_group = VGroup(window_frame, title_bar, buttons)
        
        self.play(FadeIn(window_group))
        
        # Code Content
        code_str = (
            "// Relativistic RayGen\n"
            "// 1. Aberration\n"
            "vec3 v_hat = v / beta;\n"
            "float cos_tp = dot(dir, v_hat);\n"
            "float cos_t = (cos_tp - beta) / \n"
            "              (1.0 - beta * cos_tp);\n"
            "vec3 newDir = reconstruct(v_hat, cos_t);\n\n"
            "// 2. Doppler & Headlight\n"
            "vec3 lightDir = -newDir;\n"
            "float cos_td = dot(lightDir, v_hat);\n"
            "float D = gamma * (1.0 + beta * cos_td);\n\n"
            "// 3. Shading\n"
            "payload.doppler = D; // Pass to hits\n"
            "traceRay(..., newDir, payload);"
        )
        
        code_text = Text(code_str, font="Monospace", font_size=12, t2c={"beta": YELLOW, "D": RED, "//": GREY}).move_to(window_frame)
        code_text.align_to(window_frame, UL).shift(DOWN*0.6 + RIGHT*0.3)
        
        self.play(Write(code_text))
        
        # --- Right: Visual Animation ---
        right_center = RIGHT * 3.5
        
        # Camera
        cam_dot = Dot(point=right_center + LEFT*2 + DOWN*2, color=BLUE)
        cam_label = Text("Camera", font_size=14).next_to(cam_dot, DOWN)
        
        # Velocity Vector
        vel_arrow = Arrow(cam_dot.get_center(), cam_dot.get_center() + RIGHT*1.5, color=YELLOW, buff=0)
        vel_label = Text("v", font_size=14, color=YELLOW).next_to(vel_arrow, UP)
        
        # Object
        obj = Circle(radius=0.5, color=WHITE, fill_opacity=0.5).move_to(right_center + UP*1.5)
        obj_label = Text("Scene Object", font_size=14).next_to(obj, UP)
        
        visual_group = VGroup(cam_dot, cam_label, vel_arrow, vel_label, obj, obj_label)
        self.play(FadeIn(visual_group))
        
        # --- Animation Step 1: Primary Ray (Relativistic) ---
        
        # Original Direction
        orig_ray = Arrow(cam_dot.get_center(), cam_dot.get_center() + UP*2 + RIGHT*1, color=GREY, buff=0)
        orig_text = Text("Original Dir", font_size=12, color=GREY).next_to(orig_ray.get_end(), RIGHT)
        self.play(ShowCreation(orig_ray), Write(orig_text))
        
        # Bent Direction (Aberration)
        bent_ray = Arrow(cam_dot.get_center(), obj.get_center(), color=BLUE, buff=0)
        bent_text = Text("Bent Dir", font_size=12, color=BLUE).next_to(bent_ray.get_center(), LEFT)
        self.play(TransformFromCopy(orig_ray, bent_ray), Write(bent_text))
        
        # Doppler Calculation
        doppler_tag = RoundedRectangle(width=1.2, height=0.5, corner_radius=0.1, fill_color=RED, fill_opacity=0.8)
        doppler_text = Text("D=1.5", font_size=16).move_to(doppler_tag)
        doppler_group = VGroup(doppler_tag, doppler_text).next_to(cam_dot, RIGHT)
        
        self.play(FadeIn(doppler_group))
        self.play(doppler_group.animate.move_to(obj.get_center()), run_time=1)
        
        # --- Animation Step 2: Hitting Scene ---
        # "Once we hit the scene, physics is local."
        explanation = Text("Payload 'D' is carried.\nSubsequent bounces use Scene Frame.", font_size=14, color=ORANGE).next_to(obj, RIGHT, buff=0.5)
        self.play(Write(explanation))
        
        # Bounce (Standard Light Transport)
        bounce_ray = Arrow(obj.get_center(), obj.get_center() + LEFT*2 + UP*1, color=YELLOW, buff=0)
        self.play(ShowCreation(bounce_ray))
        
        # Return Intensity
        # "Intensity = Light * D^2"
        intensity_text = Tex(r"I_{final} = I_{scene} \times D^2", font_size=20, color=RED).next_to(cam_dot, RIGHT, buff=1.0).shift(UP*1)
        self.play(Write(intensity_text))
        
        self.wait(3)
        
        self.play(
            FadeOut(window_group), FadeOut(code_text),
            FadeOut(visual_group), FadeOut(orig_ray), FadeOut(orig_text), 
            FadeOut(bent_ray), FadeOut(bent_text), FadeOut(doppler_group),
            FadeOut(explanation), FadeOut(bounce_ray), FadeOut(intensity_text),
            FadeOut(subtitle)
        )

    def results_showcase(self):
        title = Text("Part 3: Implementation Results", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        img_paths = [
            "../slide/fig/0.png",
            "../slide/fig/1.png",
            "../slide/fig/2.png",
            "../slide/fig/3.png",
            "../slide/fig/4.png",
            "../slide/fig/9.png"
        ]
        
        captions = [
            "Beta = 0.0 (Stationary)",
            "Beta = 0.1",
            "Beta = 0.2",
            "Beta = 0.3",
            "Beta = 0.4",
            "Beta = 0.9 (Extreme)"
        ]
        
        current_img = None
        current_cap = None
        
        for i, path in enumerate(img_paths):
            try:
                new_img = ImageMobject(path)
                new_img.set_height(5)
                
                new_cap = Text(captions[i], font_size=36).next_to(new_img, DOWN)
                
                if current_img is None:
                    self.play(FadeIn(new_img), Write(new_cap))
                else:
                    self.play(ReplacementTransform(current_img, new_img), ReplacementTransform(current_cap, new_cap))
                
                current_img = new_img
                current_cap = new_cap
                self.wait(1)
            except:
                fallback_text = Text(f"Image not found: {path}", font_size=24, color=RED)
                if current_img is not None:
                    self.play(FadeOut(current_img), FadeOut(current_cap))
                    current_img = None
                    current_cap = None
                self.play(FadeIn(fallback_text))
                self.wait(1)
                self.play(FadeOut(fallback_text))

        self.wait(2)
        
        # Cleanup everything before Thanks
        fade_group = VGroup()
        if current_img: fade_group.add(current_img)
        if current_cap: fade_group.add(current_cap)
        fade_group.add(title)
        
        self.play(FadeOut(fade_group))
        self.wait(1)
        
        thanks = Text("Thanks for Watching", font_size=60)
        self.play(FadeIn(thanks))
        self.wait(2)
        self.play(FadeOut(thanks))
