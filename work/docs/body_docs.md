# Body Measurement Specification

Body measurements describe the person who will wear the garment. All length values are in **centimeters** (cm) and angles are in **degrees** (deg). These measurements are extracted automatically from a 3D body mesh (SMPL) by the GarmentMeasurements pipeline.

Many garment design parameters are **ratios** that multiply a body measurement at runtime, so the final garment geometry adapts to different body shapes.

---

## Parameter Reference

### Overall Dimensions

| field | unit | method | meaning |
|---|---|---|---|
| `height` | cm | BoundingBox (Y-axis) | Total body height — Y-axis extent of the mesh bounding box. |
| `head_l` | cm | Landmark → BBox top | Vertical distance from `nape_of_neck` landmark to the top of the bounding box. `height - head_l` gives the **shoulder-to-floor height**, the effective construction space for garments. |

### Shoulder & Neck

| field | unit | method | meaning |
|---|---|---|---|
| `neck_w` | cm | VertexTrace (convex hull) | Neck opening width — length of a convex-hull vertex trace around the neck. Used as baseline for neckline width: `collar.width = 0` maps to this value. |
| `shoulder_w` | cm | LandmarkDistance | Euclidean distance between `shoulder_left` and `shoulder_right`. Determines armhole placement and maximum neckline width. |
| `shoulder_incl` | deg | AxisInclination | Angle of the shoulder line (`neck_right` → `shoulder_right`) relative to horizontal (−Y plane). Controls how bodice panels tilt at the top. |
| `armscye_depth` | cm | LandmarkDistance | Euclidean distance between `shoulder_right` and `underarm_right`. Controls armhole depth. (In construction, 2.5 cm ease is added internally: `_armscye_depth = armscye_depth + 2.5`.) |

### Arms

| field | unit | method | meaning |
|---|---|---|---|
| `arm_length` | cm | Geodesic | Geodesic (surface) distance from `shoulder_right` to `wrist_right`. `sleeve.length` is a fraction of the remaining arm length after the armhole opening. |
| `arm_pose_angle` | deg | AxisInclination | Angle of the arm axis (`shoulder_right` → `wrist_right`) relative to horizontal (−Y plane). Represents the rest pose angle of the arm in the body model; used for correct 3D sleeve placement. |
| `wrist` | cm | VertexTrace (convex hull, ring) | Wrist circumference — convex-hull perimeter of a vertex ring at the wrist. Ensures the sleeve cuff is wide enough: `end_width ≥ wrist / 2`. |

### Upper Torso

| field | unit | method | meaning |
|---|---|---|---|
| `bust` | cm | Circumference (MAX) | Bust circumference — the **maximum** horizontal cross-section perimeter at bust level, found by optimizing the cutting plane up/down within ±2 cm. `shirt.width` is a ratio of this. |
| `bust_line` | cm | Surface path (convex hull) | Surface path length on the **right** side of the torso from the shoulder–neck region down to bust level (sagittal-plane cross-section). Combined with `vert_bust_line` to derive `_bust_line`, used for collar depth and dart placement. |
| `vert_bust_line` | cm | LandmarkDistance (Y-axis) | Vertical distance from `nape_of_neck` to `bust_side_right`, projected along the Y-axis. Combined with `bust_line` to derive `_bust_line`. |
| `bust_points` | cm | LandmarkDistance | Euclidean distance between `bust_left` and `bust_right`. Used for front dart placement. |
| `underbust` | cm | Circumference | Underbust circumference — horizontal cross-section perimeter at underbust level. |
| `back_width` | cm | Partial circumference (convex hull) | Back arc length at bust level — the back half of the bust circumference, separated by `bust_side_left` / `bust_side_right` landmarks. Determines the front/back panel width split: `front_fraction = (bust - back_width) / 2 / bust`. |
| `waist` | cm | Circumference (MIN) | Waist circumference — the **minimum** horizontal cross-section perimeter at waist level, found by optimizing the cutting plane within ±2 cm. |
| `waist_line` | cm | Surface path (convex hull) | Surface path length along the **back** midline from `nape_of_neck` to `mid_waist_back`. `shirt.length` is a ratio of this — a value of 1.0 reaches exactly to the waist. |
| `waist_over_bust_line` | cm | Surface path (convex hull) | Surface path length along the **front** from shoulder to waist, passing over the bust. Used for front panel length to ensure the fabric covers the bust properly. |
| `waist_back_width` | cm | Partial circumference (convex hull) | Back arc length at waist level — the back half of the waist circumference, separated by `waist_side_left` / `waist_side_right`. Used for front/back panel width distribution at waist level. |

### Lower Body

| field | unit | method | meaning |
|---|---|---|---|
| `hips` | cm | Circumference (MAX) | Hip circumference — the **maximum** horizontal cross-section perimeter at hip level. Used for skirt/pants width. |
| `hip_back_width` | cm | Partial circumference (convex hull) | Back arc length at hip level — the back half of the hip circumference, separated by `hips_side_left` / `hips_side_right`. |
| `hips_line` | cm | LandmarkDistance (Y-axis) | Vertical distance from `waist_side_right` to `hips_side_right` along the Y-axis. Represents the waist-to-hip distance. `waistband.width` is a ratio of this. Also used to compute `_leg_length`. |
| `hip_inclination` | deg | AxisInclination | Angle of the hip side line (`hips_side_right` → `waist_side_right`) relative to vertical (X-plane). Affects pant and skirt panel shaping. (Internally halved: `_hip_inclination = hip_inclination / 2`.) |
| `bum_points` | cm | LandmarkDistance | Euclidean distance between `bum_left` and `bum_right`. Used for back dart placement in pants. |
| `crotch_hip_diff` | cm | LandmarkDistance (Y-axis) | Vertical distance from `hips_side_right` to `crotch_point` along the Y-axis. Used for pants crotch curve depth. |
| `leg_circ` | cm | Circumference (min of L/R) | Upper leg (thigh) circumference — the minimum of left and right leg measurements, each found by optimizing the cutting plane downward. `pants.flare` is relative to this. |

---

## Derived Parameters

These are computed automatically by `BodyParameters.eval_dependencies()` from the raw measurements. They appear with a `_` prefix and are used directly in garment construction.

| derived field | formula | meaning |
|---|---|---|
| `_waist_level` | `height - head_l - waist_line` | Height of the waist above the floor (cm). Used for 3D positioning of lower-body garments. |
| `_leg_length` | `_waist_level - hips_line` | Effective leg length from hip level to the floor (cm). `skirt.length`, `pants.length` are fractions of this. |
| `_base_sleeve_balance` | `shoulder_w - 2` | Adjusted shoulder width for sleeve placement (2 cm inward for better fit). |
| `_bust_line` | `2/3 × vert_bust_line + 1/3 × bust_line` | Blended bust depth — weighted average of the vertical and surface-path bust line distances. Used for collar depth (`collar.fc_depth`, `collar.bc_depth` are ratios of this) and dart vertical positioning. Falls back to `bust_line` if `vert_bust_line` is unavailable. |
| `_hip_inclination` | `hip_inclination / 2` | Halved hip inclination angle for smoother fabric distribution in pants/skirts. |
| `_shoulder_incl` | `shoulder_incl` | Shoulder inclination (passed through unchanged). |
| `_armscye_depth` | `armscye_depth + 2.5` | Armhole depth with 2.5 cm ease for comfortable fit. |

---

## How Body Measurements Map to Design Parameters

Understanding these relationships helps set accurate design values:

| design parameter | body reference | physical meaning |
|---|---|---|
| `shirt.length × waist_line` | `waist_line` | Torso coverage from shoulder. 1.0 = reaches the waist. |
| `shirt.width × bust` | `bust` | Garment width at bust level. 1.0 = exact body fit (no ease). |
| `collar.fc_depth × _bust_line` | `_bust_line` | How far the front neckline drops. 1.0 = reaches bust level. |
| `collar.bc_depth × _bust_line` | `_bust_line` | How far the back neckline drops. 1.0 = reaches bust level. |
| `collar.width` | `neck_w`, `shoulder_w` | Interpolates between `neck_w` (at 0) and shoulder edge (at 1.0). Negative values narrow below `neck_w`. |
| `sleeve.length × (arm_length - opening)` | `arm_length` | Sleeve reach from armhole. ~0.5 ≈ elbow length, 1.0 = full wrist. |
| `waistband.width × hips_line` | `hips_line` | Waistband height. 0.5 = covers half the waist-to-hip distance. |
| `waistband.waist × waist` | `waist` | Waistband circumference. 1.0 = exact waist fit. |
| `skirt.length × _leg_length` | `_leg_length` | Skirt length below waist. ~0.4 ≈ knee length. |
| `pants.length × _leg_length` | `_leg_length` | Pant leg length. ~0.5 ≈ knee, 1.0 = ankle. |
| `pants.width × min_ext` | `leg_circ`, `hips` | Crotch extension width. `min_ext = leg_circ - hips/2 + 5`. |
| `pants.flare` relative to `leg_circ` | `leg_circ` | Pant leg opening width. 1.0 = straight fit matching thigh circumference. |

---

## Example

```yaml
body:
  height: 165
  head_l: 25
  neck_w: 15
  shoulder_w: 38
  shoulder_incl: 10
  armscye_depth: 15
  arm_length: 80
  arm_pose_angle: 40
  wrist: 17
  bust: 90
  bust_line: 23
  vert_bust_line: 24
  bust_points: 21
  underbust: 83
  back_width: 45
  waist: 80
  waist_line: 36
  waist_over_bust_line: 43
  waist_back_width: 37
  hips: 107
  hip_back_width: 55
  hips_line: 22
  hip_inclination: 6
  bum_points: 16
  crotch_hip_diff: 10.5
  leg_circ: 64
```

**Derived values for this body:**

| derived | value | calculation |
|---|---|---|
| `_waist_level` | 104 cm | 165 − 25 − 36 |
| `_leg_length` | 82 cm | 104 − 22 |
| `_bust_line` | 23.67 cm | 2/3 × 24 + 1/3 × 23 |
| `_armscye_depth` | 17.5 cm | 15 + 2.5 |
| `_hip_inclination` | 3 deg | 6 / 2 |

A `skirt.length` of 0.4 → 0.4 × 82 = ~33 cm below the waist (approximately knee length).
A `shirt.length` of 1.0 → 1.0 × 36 = 36 cm, reaching exactly to the waist.
