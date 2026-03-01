# Garment Design Parameter Specification

A YAML file following this specification fully describes one garment outfit — its structure, shape, and style. The file is a nested key-value structure where every leaf node holds a concrete value (number, boolean, or string).

## How It Works

A garment is composed of **parts**: an optional upper body (shirt/top), an optional lower body (skirt/pants), and optional accessories (waistband, collar, sleeves, cuffs). The `meta` section declares which parts are present; each active part has a corresponding **section** of parameters.

**Key principles:**

- `meta` is always required. It determines which other sections must appear.
- Sections for inactive parts should be omitted.
- `null` means "none / disabled".
- All numeric values must stay within their specified `[min, max]` range.
- Every parameter in an active section must be provided — do not omit any.

## Value Types

In the parameter definitions below, types are annotated as:

- `float [min, max]` — floating-point number within range
- `int [min, max]` — integer within range
- `bool` — `true` or `false`
- `A | B | C` — pick exactly one from the listed options
- `A | B | null` — pick one, or `null` to disable

Most numeric parameters are **ratios** (multiplied by a body measurement at runtime). A few are **absolute** (cm or degrees) — noted where applicable.

---

## Section Activation Rules

The values in `meta` determine which sections to include:

| meta field | value | required sections |
|---|---|---|
| `upper` | `Shirt` | `shirt`, `collar`, `sleeve` |
| `upper` | `FittedShirt` | `shirt` (`length` is ignored), `collar`, `sleeve` |
| `upper` | `null` | *(none)* |
| `wb` | `StraightWB` or `FittedWB` | `waistband` |
| `wb` | `null` | *(none)* |
| `bottom` | `Skirt2` | `skirt` |
| `bottom` | `SkirtCircle`, `AsymmSkirtCircle`, or `SkirtManyPanels` | `flare-skirt` |
| `bottom` | `PencilSkirt` | `pencil-skirt` |
| `bottom` | `GodetSkirt` | `godet-skirt` + the base skirt section (`skirt` or `pencil-skirt`, per `godet-skirt.base`) |
| `bottom` | `SkirtLevels` | `levels-skirt` |
| `bottom` | `Pants` | `pants` |
| `bottom` | `null` | *(none)* |

The `left` section is always present. If `left.enable_asym: true`, also include `left.shirt`, `left.collar`, `left.sleeve`.

---

## Parameter Reference

### meta *(always required)*

Declares which garment parts exist and how they connect.

```yaml
meta:
  upper: Shirt | FittedShirt | null
  wb: StraightWB | FittedWB | null
  bottom: SkirtCircle | AsymmSkirtCircle | GodetSkirt | Pants
          | Skirt2 | SkirtManyPanels | PencilSkirt | SkirtLevels | null
  connected: bool
```

| field | meaning |
|---|---|
| `upper` | `Shirt` = regular top (t-shirt, blouse); `FittedShirt` = body-hugging top (tube top, bustier); `null` = no upper |
| `wb` | `StraightWB` = straight waistband; `FittedWB` = shaped/fitted waistband; `null` = no waistband |
| `bottom` | lower-body garment type (see sections below); `null` = no lower |
| `connected` | `true` = upper and lower are sewn together as one piece (dress, jumpsuit); `false` = separate pieces. When `true`, set `shirt.length` to a small value (e.g. 0.5) |

### waistband *(when `wb` is not null)*

```yaml
waistband:
  waist: float [1.0, 2.0]    # waist fit ratio (× body waist); 1.0 = body-tight, 1.5 = comfortable, 2.0 = very loose
  width: float [0.1, 1.0]    # band height ratio (× hip-to-waist distance); 0.1 = narrow strip, 1.0 = covers entire hip-to-waist span
```

### shirt *(when `upper` is not null)*

Controls the torso piece.

```yaml
shirt:
  strapless: bool             # strapless/tube top; only effective when upper = FittedShirt (ignored for Shirt)
  length: float [0.5, 3.5]   # length ratio (× shoulder-to-waist distance); 0.5 = cropped, 1.0 = at waist, 1.2 = below waist, 3.0 = long tunic
  width: float [1.0, 1.3]    # width ratio (× bust); 1.0 = fitted, 1.3 = oversized
  flare: float [0.7, 1.6]    # hem-to-chest ratio; <1 = tapered, 1 = straight, >1 = A-line/flared
```

> When `upper = FittedShirt`, `length` is still present in the YAML but ignored — the tight-fit bodice construction determines length from body measurements.

### collar *(when `upper` is not null)*

Defines the neckline shape and optional collar attachment. Always provide this section when `upper` is set, even when `strapless: true` — the neckline depth values are still used internally for strapless construction.

```yaml
collar:
  f_collar: CircleNeckHalf | CurvyNeckHalf | VNeckHalf | SquareNeckHalf
            | TrapezoidNeckHalf | CircleArcNeckHalf | Bezier2NeckHalf
  b_collar: (same options as f_collar)
  width: float [-0.5, 1.0]        # neckline width factor; 0 = at neck, 1 = max shoulder width, negative = narrower than neck
  fc_depth: float [0.3, 2.0]      # front neckline depth ratio (× bust-line height)
  bc_depth: float [0.0, 2.0]      # back neckline depth ratio (× bust-line height); 0 = no back neckline drop
  fc_angle: int [70, 110]         # front neckline angle in degrees (for Trapezoid / CircleArc)
  bc_angle: int [70, 110]         # back neckline angle in degrees
  f_bezier_x: float [0.05, 0.95]  # front Bezier control point x, normalized (for Bezier2)
  f_bezier_y: float [0.05, 0.95]  # front Bezier control point y
  b_bezier_x: float [0.05, 0.95]  # back Bezier control point x
  b_bezier_y: float [0.05, 0.95]  # back Bezier control point y
  f_flip_curve: bool               # mirror the front neckline curve
  b_flip_curve: bool               # mirror the back neckline curve
  component:
    style: Turtle | SimpleLapel | Hood2Panels | null  # collar attachment; null = none
    depth: int [2, 8]              # attachment height (cm, absolute)
    lapel_standing: bool           # whether the lapel stands up
    hood_depth: float [1.0, 2.0]  # hood depth ratio
    hood_length: float [1.0, 1.5] # hood length ratio (× head length)
```

**Neckline types:**

| type | shape | extra params needed |
|---|---|---|
| `CircleNeckHalf` | round / crew neck | — |
| `CurvyNeckHalf` | smooth curved neck | `f_flip_curve`, `b_flip_curve` |
| `VNeckHalf` | V-neck | — |
| `SquareNeckHalf` | square neck | — |
| `TrapezoidNeckHalf` | trapezoid neck | `fc_angle`, `bc_angle` |
| `CircleArcNeckHalf` | elliptical arc neck | `fc_angle`, `bc_angle`, `f_flip_curve`, `b_flip_curve` |
| `Bezier2NeckHalf` | quadratic Bezier curve neck | `f_bezier_*`, `b_bezier_*`, `f_flip_curve`, `b_flip_curve` |

> All neckline types use `width`, `fc_depth`, `bc_depth`. The angle, Bezier, and flip params are always present in the YAML but only take effect for the matching type.

### sleeve *(when `upper` is not null)*

```yaml
sleeve:
  sleeveless: bool                                     # true = no sleeves (armhole-only cutout)
  armhole_shape: ArmholeSquare | ArmholeAngle | ArmholeCurve  # only effective when sleeveless; with sleeves, always ArmholeCurve
  length: float [0.1, 1.15]       # fraction of arm length; 0.2 = short, 0.5 = elbow, 0.75 = 3/4, 1.0 = full
  connecting_width: float [0.0, 2.0]   # armhole depth factor; controls how far the sleeve extends into the bodice
  end_width: float [0.2, 2.0]     # cuff opening ratio (× armhole width); <1 = narrowing, 1 = straight, >1 = bell/flared
  sleeve_angle: int [10, 50]      # rest angle at shoulder (degrees, absolute); smaller = closer to body
  opening_dir_mix: float [-0.9, 0.8]   # cuff edge direction blend; negative = more horizontal, positive = more downward
  smoothing_coeff: float [0.1, 0.4]    # armhole curve smoothness (for non-curve shapes)
  standing_shoulder: bool          # puff shoulder effect
  standing_shoulder_len: float [4, 10]  # puff extent (cm, absolute)
  connect_ruffle: float [1.0, 2.0]     # shoulder ruffle; 1.0 = none, 2.0 = heavy
  cuff:
    type: CuffBand | CuffSkirt | CuffBandSkirt | null   # cuff style; null = plain edge
    top_ruffle: float [1.0, 3.0]       # ruffle at top of cuff
    cuff_len: float [0.05, 0.9]        # cuff length as fraction of arm length
    skirt_fraction: float [0.1, 0.9]   # skirt portion of cuff (for CuffSkirt / CuffBandSkirt)
    skirt_flare: float [1.0, 2.0]      # cuff skirt flare
    skirt_ruffle: float [1.0, 1.5]     # cuff skirt ruffle
```

> When `sleeveless: true`, `armhole_shape` controls the armhole cutout shape (all three options available); other sleeve params can use defaults. When `sleeveless: false`, the armhole is always `ArmholeCurve` regardless of `armhole_shape`.

### left *(asymmetric design)*

By default the garment is symmetric (left side mirrors right). Set `enable_asym: true` to give the left side independent parameters.

```yaml
left:
  enable_asym: bool   # false = symmetric; true = left side has its own params
```

When `enable_asym: true`, add these sub-sections under `left`:
- `left.shirt` — same fields as `shirt` but **without `length`** (length is shared)
- `left.collar` — same fields as `collar` but **without `fc_depth`, `bc_depth`, and `component`** (depth is shared with right side; collar attachment is disabled for asymmetric designs)
- `left.sleeve` — same fields as `sleeve`

The main `shirt`, `collar`, `sleeve` sections define the **right** side.

### skirt *(when `bottom = Skirt2`)*

A basic straight skirt with optional flare and slit.

```yaml
skirt:
  length: float [-0.2, 0.95]   # fraction of leg length; negative = above hip, 0 = at hip, 0.4 = knee, 0.7 = mid-calf, 0.95 = floor
  rise: float [0.5, 1.0]       # waist rise; 0.5 = low-rise, 0.75 = mid, 1.0 = high-waist
  ruffle: float [1.0, 2.0]     # waist gather/ruffle multiplier; 1.0 = none, 2.0 = double-gathered
  bottom_cut: float [0.0, 0.9] # hem slit depth ratio (× skirt length); 0 = no slit
  flare: int [0, 20]           # hem flare angle (degrees, absolute)
```

### flare-skirt *(when `bottom` = SkirtCircle | AsymmSkirtCircle | SkirtManyPanels)*

A full/circle skirt. Sub-fields activate depending on the exact `bottom` type.

```yaml
flare-skirt:
  length: float [-0.2, 0.95]   # fraction of leg length; negative = above hip
  rise: float [0.5, 1.0]       # waist rise; 0.5 = low-rise, 1.0 = high-waist
  suns: float [0.1, 1.95]      # fullness; 0.1 = slight flare, 1.0 = full circle, 1.95 = extreme gather
  skirt-many-panels:            # only for SkirtManyPanels
    n_panels: int [4, 15]
    panel_curve: -0.35 | -0.25 | -0.15 | 0 | 0.15 | 0.25 | 0.35 | 0.45  # seam curvature
  asymm:                        # only for AsymmSkirtCircle
    front_length: float [0.1, 0.9]   # front-to-back length ratio
  cut:
    add: bool                   # whether to add a slit/cutout
    depth: float [0.05, 0.95]  # slit depth (fraction of skirt length)
    width: float [0.05, 0.4]   # slit width (fraction of skirt length)
    place: float [-1, 1]       # position; -1 = center back, 0 = side, 1 = center front
```

### godet-skirt *(when `bottom = GodetSkirt`)*

A skirt with triangular fabric inserts at the hem for added flare.

```yaml
godet-skirt:
  base: Skirt2 | PencilSkirt        # base skirt type
  insert_w: int [10, 50]            # insert width (cm, absolute)
  insert_depth: int [10, 50]        # insert depth (cm, absolute)
  num_inserts: 4 | 6 | 8 | 10 | 12 # number of inserts
  cuts_distance: int [0, 10]        # spacing between inserts (cm, absolute)
```

> You must also include the section for the base skirt (`skirt` if `base = Skirt2`, or `pencil-skirt` if `base = PencilSkirt`).

### pencil-skirt *(when `bottom = PencilSkirt`)*

A fitted, narrow skirt.

```yaml
pencil-skirt:
  length: float [0.2, 0.95]    # fraction of leg length; 0.4 = above knee, 0.5 = knee, 0.95 = floor
  rise: float [0.5, 1.0]       # waist rise; 0.5 = low-rise, 1.0 = high-waist
  flare: float [0.6, 1.5]      # hem width ratio; <1 = tight/hobble, 1 = straight, >1 = slight flare
  low_angle: int [-30, 30]     # hem tilt angle (degrees, absolute); 0 = level
  front_slit: float [0.0, 0.9] # front center slit depth (fraction of skirt length); 0 = no slit
  back_slit: float [0.0, 0.9]  # back center slit depth (fraction of skirt length); 0 = no slit
  left_slit: float [0.0, 0.9]  # left side opening (fraction of side edge); 0 = no slit
  right_slit: float [0.0, 0.9] # right side opening (fraction of side edge); 0 = no slit
  style_side_cut: Sun | SIGGRAPH_logo | null   # decorative side cutout
```

### levels-skirt *(when `bottom = SkirtLevels`)*

A tiered/layered skirt with a top tier and one or more lower tiers.

```yaml
levels-skirt:
  base: Skirt2 | PencilSkirt | SkirtCircle | AsymmSkirtCircle   # top tier style
  level: Skirt2 | SkirtCircle | AsymmSkirtCircle                 # lower tiers style
  num_levels: int [1, 5]           # number of lower tiers (total tiers = num_levels + 1)
  level_ruffle: float [1.0, 1.7]  # ruffle per tier
  length: float [0.2, 0.95]       # total skirt length (fraction of leg length)
  rise: float [0.5, 1.0]          # waist rise; 0.5 = low-rise, 1.0 = high-waist
  base_length_frac: float [0.2, 0.8]  # top tier's share of total length
```

### pants *(when `bottom = Pants`)*

```yaml
pants:
  length: float [0.2, 0.9]     # fraction of leg length; 0.2 = micro shorts, 0.45 = knee, 0.7 = cropped, 0.9 = full-length
  width: float [1.0, 1.5]      # crotch/hip width factor; 1.0 = slim fit, 1.5 = wide/relaxed
  flare: float [0.5, 1.2]      # leg opening ratio (× leg circumference); <1 = tapered, 1 = straight, >1 = flared/bell-bottom
  rise: float [0.5, 1.0]       # waist rise; 0.5 = low-rise, 0.75 = mid, 1.0 = high-waist
  cuff:
    type: CuffBand | CuffSkirt | CuffBandSkirt | null   # cuff style; null = plain edge
    top_ruffle: float [1.0, 2.0]       # ruffle at top of cuff
    cuff_len: float [0.05, 0.9]        # cuff length as fraction of leg length
    skirt_fraction: float [0.1, 0.9]   # skirt portion of cuff (for CuffSkirt / CuffBandSkirt)
    skirt_flare: float [1.0, 2.0]      # cuff skirt flare
    skirt_ruffle: float [1.0, 1.5]     # cuff skirt ruffle
```

---

## Rules Summary

1. All numeric values must be within the specified `[min, max]` range.
2. Every parameter in an active section must be provided.
3. When `connected: true` (one-piece dress), set `shirt.length` small (e.g. 0.5).
4. Always provide `collar` and `sleeve` when `upper` is not null — even when `strapless: true`.
5. When `sleeveless: true`, `armhole_shape` determines the cutout shape. When `sleeveless: false`, `ArmholeCurve` is always used.
6. When `left.enable_asym: false`, omit `left.shirt`, `left.collar`, `left.sleeve`.
7. `GodetSkirt` requires an additional base skirt section; `SkirtLevels` uses `levels-skirt` params.
8. Output only the YAML content. No extra text or explanation.

---

## Examples

### Short-sleeve V-neck dress

```yaml
meta:
  upper: Shirt
  wb: FittedWB
  bottom: SkirtCircle
  connected: true
waistband:
  waist: 1.0
  width: 0.3
shirt:
  strapless: false
  length: 0.5
  width: 1.05
  flare: 1.0
collar:
  f_collar: VNeckHalf
  b_collar: CircleNeckHalf
  width: 0.2
  fc_depth: 0.8
  bc_depth: 0.3
  fc_angle: 90
  bc_angle: 90
  f_bezier_x: 0.3
  f_bezier_y: 0.55
  b_bezier_x: 0.15
  b_bezier_y: 0.1
  f_flip_curve: false
  b_flip_curve: false
  component:
    style: null
    depth: 7
    lapel_standing: false
    hood_depth: 1.0
    hood_length: 1.0
sleeve:
  sleeveless: false
  armhole_shape: ArmholeCurve
  length: 0.2
  connecting_width: 0.2
  end_width: 1.0
  sleeve_angle: 30
  opening_dir_mix: 0.1
  standing_shoulder: false
  standing_shoulder_len: 5.0
  connect_ruffle: 1.0
  smoothing_coeff: 0.25
  cuff:
    type: null
    top_ruffle: 1.0
    cuff_len: 0.1
    skirt_fraction: 0.5
    skirt_flare: 1.2
    skirt_ruffle: 1.0
left:
  enable_asym: false
flare-skirt:
  length: 0.4
  rise: 1.0
  suns: 0.75
  skirt-many-panels:
    n_panels: 4
    panel_curve: 0
  asymm:
    front_length: 0.5
  cut:
    add: false
    depth: 0.5
    width: 0.1
    place: -0.5
```

### Basic T-shirt (no bottom)

```yaml
meta:
  upper: Shirt
  wb: null
  bottom: null
  connected: false
shirt:
  strapless: false
  length: 1.2
  width: 1.05
  flare: 1.0
collar:
  f_collar: CircleNeckHalf
  b_collar: CircleNeckHalf
  width: 0.2
  fc_depth: 0.4
  bc_depth: 0.0
  fc_angle: 95
  bc_angle: 95
  f_bezier_x: 0.3
  f_bezier_y: 0.55
  b_bezier_x: 0.15
  b_bezier_y: 0.1
  f_flip_curve: false
  b_flip_curve: false
  component:
    style: null
    depth: 7
    lapel_standing: false
    hood_depth: 1.0
    hood_length: 1.0
sleeve:
  sleeveless: false
  armhole_shape: ArmholeCurve
  length: 0.3
  connecting_width: 0.2
  end_width: 1.0
  sleeve_angle: 10
  opening_dir_mix: 0.1
  standing_shoulder: false
  standing_shoulder_len: 5.0
  connect_ruffle: 1.0
  smoothing_coeff: 0.25
  cuff:
    type: null
    top_ruffle: 1.0
    cuff_len: 0.1
    skirt_fraction: 0.5
    skirt_flare: 1.2
    skirt_ruffle: 1.0
left:
  enable_asym: false
```

### Blouse + pencil skirt (separates)

```yaml
meta:
  upper: Shirt
  wb: FittedWB
  bottom: PencilSkirt
  connected: false
waistband:
  waist: 1.0
  width: 0.2
shirt:
  strapless: false
  length: 1.5
  width: 1.1
  flare: 1.0
collar:
  f_collar: VNeckHalf
  b_collar: CircleNeckHalf
  width: 0.3
  fc_depth: 0.6
  bc_depth: 0.2
  fc_angle: 90
  bc_angle: 90
  f_bezier_x: 0.3
  f_bezier_y: 0.55
  b_bezier_x: 0.15
  b_bezier_y: 0.1
  f_flip_curve: false
  b_flip_curve: false
  component:
    style: null
    depth: 7
    lapel_standing: false
    hood_depth: 1.0
    hood_length: 1.0
sleeve:
  sleeveless: false
  armhole_shape: ArmholeCurve
  length: 0.75
  connecting_width: 0.2
  end_width: 1.0
  sleeve_angle: 20
  opening_dir_mix: 0.1
  standing_shoulder: false
  standing_shoulder_len: 5.0
  connect_ruffle: 1.0
  smoothing_coeff: 0.25
  cuff:
    type: null
    top_ruffle: 1.0
    cuff_len: 0.1
    skirt_fraction: 0.5
    skirt_flare: 1.2
    skirt_ruffle: 1.0
left:
  enable_asym: false
pencil-skirt:
  length: 0.5
  rise: 0.85
  flare: 1.0
  low_angle: 0
  front_slit: 0.0
  back_slit: 0.2
  left_slit: 0.0
  right_slit: 0.0
  style_side_cut: null
```

### Wide-leg trousers (no top)

```yaml
meta:
  upper: null
  wb: StraightWB
  bottom: Pants
  connected: false
waistband:
  waist: 1.3
  width: 0.4
pants:
  length: 0.85
  width: 1.4
  flare: 1.0
  rise: 0.9
  cuff:
    type: null
    top_ruffle: 1.0
    cuff_len: 0.1
    skirt_fraction: 0.5
    skirt_flare: 1.2
    skirt_ruffle: 1.0
left:
  enable_asym: false
```
