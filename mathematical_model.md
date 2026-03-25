# 🧮 Formal Mathematical Model for ROBEX System

This document outlines the complete mathematical framework governing the AI and logical operations within the ROBEX system. It incorporates the general Set Theory system flow, and the concrete mathematical algorithms used for Detection, Recognition, Liveness, and Anti-Spoofing.

## 1. System Set Theory Representation
Based on the general system model (Inputs, Processes, Outputs):

*   **Inputs ($I$)**: The set of incoming video frames streaming from the ESP32-CAM.
    
    $$
    I = \{ f_t \mid t = 0, 1, 2, \dots, T \}
    $$
    
    where $f_t$ is a $W \times H \times 3$ BGR image matrix at time $t$.

*   **Outputs ($O$)**: The set of operational endpoints.
    
    $$
    O = \{ \text{ID}_{\text{identified}}, \text{Action}_{\text{motor}}, \text{Audio}_{\text{out}}, \text{Database}_{\text{log}} \}
    $$

*   **Processes ($P$)**: The mapping functions that transform $I \to O$.
    
    $$
    P = \{ F_{\text{detect}}, F_{\text{liveness}}, F_{\text{recognize}}, F_{\text{antispoof}} \}
    $$

**The Core Validation Constraint:**
The system ensures attendance $A$ is marked for student $u$ only if the following logical condition is met:

$$
A_u = \begin{cases} 
1 & \text{if } F_{\text{detect}}(f_t) \land F_{\text{liveness}}(f_t) \land \left(F_{\text{recognize}}(f_t)=u\right) \land \neg F_{\text{antispoof}}(f_t) \\
0 & \text{otherwise} 
\end{cases}
$$

*(Meaning: Face is found AND Person Blinks AND Face matches Database AND No Cell Phone detected)*

---

## 2. Face Detection (Haar Cascades)

Haar Cascades calculate the contrast difference between adjacent rectangular regions of the face (e.g., eye sockets are darker than cheekbones).

**The Integral Image ($ii$)** (Allows instant, $O(1)$ computation time):

$$
ii(x, y) = \sum_{x' \le x, y' \le y} i(x', y')
$$

where $i(x,y)$ is the original pixel intensity.

**Feature Evaluation ($f(x)$)**:
Calculates the numerical difference between dark and light regions.

$$
f(x) = \sum_{(x,y) \in R_{\text{white}}} i(x,y) \ - \sum_{(x,y) \in R_{\text{dark}}} i(x,y)
$$

**AdaBoost Classifier Algorithm**:
Combines multiple weak algorithms $h_t(x)$ into a highly accurate strong bounding-box classifier $H(x)$:

$$
H(x) = \text{sgn} \left( \sum_{t=1}^{T} \alpha_t h_t(x) \right)
$$

where $\alpha_t$ is the training weight of the weak classifier.

---

## 3. Liveness Detection via Eye Aspect Ratio (EAR)

To prevent photo-spoofing, the system maps 6 facial landmarks (points $p_1$ to $p_6$) on the perimeter of the user's eye and computes their geometric distances.

**Euclidean Distance**:
Between any two mapped points $p_a(x_a, y_a)$ and $p_b(x_b, y_b)$:

$$
d(p_a, p_b) = \sqrt{(x_a - x_b)^2 + (y_a - y_b)^2}
$$

**EAR Equation**:

$$
EAR = \frac{d(p_2, p_6) + d(p_3, p_5)}{2 \cdot d(p_1, p_4)}
$$

*   **Numerator**: The sum of the two vertical distances across the top and bottom eyelids.
*   **Denominator**: Twice the horizontal distance from the inner to outer edge of the eye (used to balance out varying distance from the camera).
*   **Mathematical Condition for Liveness**: A blink is confirmed if $EAR < \tau_{\text{blink}}$ (where the threshold $\tau_{\text{blink}} \approx 0.2$) for a frame, indicating the vertical distance went to $0$.

---

## 4. Face Recognition (LBPH - Local Binary Patterns Histograms)

LBPH mathematically extracts texture vectors from the face bounding box, untouched by varying brightness or shadows.

**LBP Operator Vector**:
For a central pixel $i_c$ and its $P$ neighbor pixels $i_p$ on a radius $R$:

$$
LBP_{P, R}(x_c, y_c) = \sum_{p=0}^{P-1} s(i_p - i_c) 2^p
$$

where the Binary Thresholding function $s(x)$ is:

$$
s(x) = \begin{cases} 
1 & \text{if } x \ge 0 \\
0 & \text{if } x < 0 
\end{cases}
$$

**Histogram Matching Distance ($D$)**:
To find who the person is, the system calculates the **Chi-Square distance** between the camera's generated histogram $H_{\text{cam}}$ and a saved database histogram $H_{\text{db}}$:

$$
D(H_{\text{cam}}, H_{\text{db}}) = \sum_{i=1}^{n} \frac{(H_{\text{cam}}(i) - H_{\text{db}}(i))^2}{H_{\text{cam}}(i) + H_{\text{db}}(i)}
$$

*   The ID with the minimum distance $D_{\text{min}}$ is the predicted identity. A lower numerical distance is mathematically interpreted as a stronger visual match.

---

## 5. Anti-Spoofing (YOLOv8 Object Detection)

YOLOv8 runs the frame matrix through Deep Neural Network weights to detect electronic devices (which scammers use to hold up fake photos).

YOLO divides the image into an $S \times S$ grid. For each grid cell, it predicts Boundary Boxes and Class Probabilities.

**Confidence Mathematical Score**:

$$
\text{Confidence} = P(\text{Object}) \times \text{IoU}_{\text{truth}}^{\text{pred}}
$$

where $\text{IoU}$ stands for *Intersection over Union* (Area of Overlap divided by Area of Union).

**Class-specific Safety Condition**:

$$
CS_i = P(\text{Class}_i \mid \text{Object}) \times \text{Confidence}
$$

If any bounding box possesses $CS_{\text{phone}} > \tau_{\text{phone}}$, the system logically triggers $F_{\text{antispoof}}(f_t) = \text{True}$. The core constraint (from Section 1) instantly fails, refusing to mark attendance.
