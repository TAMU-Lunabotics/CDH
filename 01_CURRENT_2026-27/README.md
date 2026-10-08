# 2026–27 CDH — Current Season

**This is the folder to use for current Lunabotics CDH work.**

This folder contains current-season planning and a **working, disarmed driver candidate**. No production 2026–27 CDH driver has been approved yet.

## What is in this folder?

| File | Plain-English purpose |
|---|---|
| [01_Competition_Rules.md](01_Competition_Rules.md) | Competition rules that directly affect CDH/software |
| [02_Interfaces.md](02_Interfaces.md) | What information/commands CDH exchanges with Electrical, GNC, and Mission Control |
| [03_Open_Questions.md](03_Open_Questions.md) | Questions CDH still needs answered by other teams |
| [04_Decisions.md](04_Decisions.md) | Approved current-season decisions |
| [05_Setup.md](05_Setup.md) | How a CDH member sets up ROS 2 and the development environment |
| [06_Guarded_Drivers](06_Guarded_Drivers/) | Disarmed RoboClaw/Pico integration candidate with command expiry and tests |

## Current Working Baseline

The working development environment is:
- Ubuntu 22.04
- ROS 2 Humble
- C++ and Python
- GitHub + colcon
- PlatformIO / Arduino tooling when embedded-controller work is required

These are the **working 2026–27 development assumptions**. Hardware and architecture inherited from 2025–26 are not automatically approved for this season.

## Simple Rule

If something is being developed **for this year's robot**, it belongs here.

If something came from the **2025–26 robot**, keep it in [02_OLD_2025-26](../02_OLD_2025-26/) until the team deliberately chooses to reuse it.
