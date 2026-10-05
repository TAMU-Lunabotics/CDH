# TAMU Lunabotics — Command & Data Handling (CDH)

This repository contains the **CDH team's software, interfaces, setup information, and useful historical code**.

## Start Here

You only need to understand two folders:

| Folder | What it is | Use it for |
|---|---|---|
| **[01_CURRENT_2026-27](01_CURRENT_2026-27/)** | This season | Current requirements, interfaces, decisions, setup, and future current-season code |
| **[02_OLD_2025-26](02_OLD_2025-26/)** | Last season | Old working code kept only as a reference |

> **Important:** Anything inside `02_OLD_2025-26` is old code. Do not assume it is part of the 2026–27 robot.

## What CDH Does

In simple terms, CDH connects the robot's **computers, sensors, motor controllers, autonomy software, operator controls, telemetry, and communications** so the whole robot can work together.

CDH works closely with:
- **Electrical** for wiring, power, sensors, and motor-controller interfaces.
- **GNC** for localization, autonomy, motion commands, maps, and sensor data.
- **Communications / Mission Control** for telemetry, operator control, and competition networking.

## Where Should I Look?

| I want to... | Go here |
|---|---|
| Understand what CDH is doing this year | [Current season overview](01_CURRENT_2026-27/README.md) |
| See competition-related CDH rules | [Competition rules](01_CURRENT_2026-27/01_Competition_Rules.md) |
| See what data CDH exchanges with other teams | [Interfaces](01_CURRENT_2026-27/02_Interfaces.md) |
| See unanswered questions | [Open questions](01_CURRENT_2026-27/03_Open_Questions.md) |
| See approved decisions | [Decision log](01_CURRENT_2026-27/04_Decisions.md) |
| Set up a development computer | [Development setup](01_CURRENT_2026-27/05_Setup.md) |
| Look at last year's code | [2025–26 archive](02_OLD_2025-26/README.md) |

The `.github` folder and `.gitignore` file are GitHub/developer housekeeping files and can be ignored by most members.
