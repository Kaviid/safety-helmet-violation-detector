# Problem Definition

## Problem Statement
Build a supervised object detection model that finds construction workers in CCTV video and checks whether each one is wearing a safety helmet. The system should flag workers without helmets so the site can prevent head injuries.

## Classes
Classes are the labels the model can output. I chose two:
- **helmet**: a worker's head with a safety helmet
- **no_helmet**: a worker's head without a safety helmet

## Success Targets
| Metric | Target | Why |
|---|---|---|
| Recall (no_helmet) | ≥ 90% | Catch at least 9 of 10 unsafe workers |
| Precision (no_helmet) | ≥ 80% | Keep false alarms low enough that people don't ignore the alerts |
| mAP@50 | ≥ 85% | Overall detection quality |
| Speed | ≥ 15 FPS on RTX 4050 | Fast enough for live CCTV |

## Constraints
Constraints are the real-world problems this model must handle:
- CCTV cameras sit high up, so they often see the top of the workers' heads
- Workers far away appear as just a few pixels
- Lighting changes: sunlight, night, shade, indoor lights
- Caps, hoodies and hair can look like helmets, so the model must separate them correctly
- Workers are sometimes blocked by machines or other workers
- Video quality: blur, low resolution, compression
- Helmets come in different colours: red, yellow, blue, white and orange

## Data
| Dataset | Images | Format | Notes |
|---|---|---|---|
| Kaggle Hard Hat | 5,000 | XML (Pascal VOC) | helmet → helmet, head → no_helmet, person → dropped |
| Top-view dataset | 752 | YOLO | Helmet colours merged into one helmet class |