# 2026–27 Competition Constraints — CDH-Relevant

**Status: CURRENT — 2026–27 competition requirements**

This file contains only the rules that materially affect CDH/software integration. The official NASA guidebook remains authoritative.

## Communications
- Robot operations in the Artemis Arena use the assigned competition wireless configuration / Channel 1.
- Teams must be able to configure to Channel 1 within **15 minutes of notification** for real-time scheduling changes.
- The team must demonstrate wireless robot control during communications checkout.
- Wireless-emission equipment must be identifiable/documented as required by inspection.

## Mission Control / Autonomy Visibility
For travel autonomy, Mission Control must show **real-time obstacle detection, obstacle mapping, and the resulting path planning** so judges can verify that breadcrumb/remote-defined waypoint behavior is not being used.

CDH therefore needs a reliable path for:
- perception/map/path telemetry from GNC
- operator/judge-visible visualization
- autonomy/manual state
- health/status and failure visibility

## Operations / Safety Integration
- The robot must stop operations when the required power-off command is sent or when directed by arena personnel.
- Software/command handling must not obscure the distinction between hands-free autonomy and remote control.
- Competition runs are **15 minutes**, so logs, telemetry, startup, recovery, and operator tooling should be designed around the actual run timeline.

## Current-Season Rule
Older 2025–26 communications assumptions or UI behavior are not authoritative for 2026–27. Verify implementation against the current guidebook and official updates.
