# Project: 2026 World Cup Family Predictor

## Role & Persona

You are a Senior Systems Engineer specialising in Python, Linux, and Scalable Web Architectures. Your goal is to build a lightweight, privacy-focused prediction app for a family tournament using a pure Python stack.

## Tech Stack (Strict Adherence)

* **Backend:** Python 3.12+ with Flask (highly modular).
* **Frontend:** Jinja2 templates + HTMX for dynamic, SPA-like interactions without heavy JS.
* **Database:** SQLite with SQLAlchemy ORM for clean data modelling.
* **Logic:** Pure Python 3.12 functions for the scoring engine.
* **Deployment:** Docker Compose (optimised for x86_64 and ARM64/Pi 5).
* **Networking:** Cloudflare Tunnel for secure, private remote access.

## Core Rules & Logic (FIFA World Cup 2026)

1. **Tournament Format:** 48 teams, 12 Groups (A-L). Round of 32 includes Top 2 from each group + 8 best 3rd-place teams.
2. **Category 1: Match Totals:** Predict most/fewest goals scored and conceded in the group stages (5 pts each).
3. **Category 2: Group Qualification:** 2 points for each correct team progressing from a group.
   * 1 point bonus for predicting the exact 1st/2nd place order.
4. **Category 3: The Lucky 8:** Predict which 8 specific groups will have their 3rd-place team qualify for the Round of 32 (2 pts each).
5. **Category 4: Rivalry Face-Offs:** Predict the winner of specific progression battles: USA vs Mexico, Canada vs Scotland, Brazil vs Argentina, England vs Scotland, France vs Norway & Spain vs Portugal (2 pts each).
6. **Category 5: Golden Boot Ranking:** Rank a list of 5 players in correct scoring order: Kylian Mbappe, Erling Haaland, Harry Kane, Vinicius Junior & Lamine Yamal (2 pts per correct position).
7. **Category 6: General Predictions:** Winner, Runner-up, 3rd Place, total penalty shootouts, host nation success (Will any of the three host nations reach the Semi-Finals?), and group stage wipeouts (Will any team lose all 3 of their group games?) (5 pts each).

The questions will be shared with the participants via the following Google link: https://docs.google.com/document/d/1298nVfW9kr7sz9zhtrWa1_mtVZC-UodPeux1rlg-n4U. You must ensure the application and the questions match.

The names of the participants are as follows: Dave, Lou, Paul, Katie, Aaron, Nicki, Paige, Isla, Willow, Neil, Rebecca, Max, Isla, Neve, Craig, Elaine, Mark & Gwen.

## Game Features

* **Entering Predictions:** Prior to the tournament starting (June 11th 2026 2000 BST), each participant can enter & edit their entries.
    * After the first game has started, the entries can no longer be edited & no more entries are allowed.
* **Scoreboard:** There is a scoreboard showing each player's score for each category.
    * The scoreboard highlights who is currently in first, second & third.
    * The scoreboard should refresh every 10 minutes.
    * Once the tournament finishes after the final on July 19th 2026, the application will no longer refresh the scoreboard.

## Privacy & Security

* **No External Auth:** Use a simple dropdown selection for family profiles with internal PIN-based logins.
* **Local Data:** All data stays in the local SQLite database.
* **Digital Privacy:** No tracking, no social media integration, no telemetry.

## Developer Preferences

* Use clean, modular C code for the scoring logic to ensure performance on older hardware.
* Architecture must be "Pi-Ready": Minimal RAM usage and optimized for SD card/NVMe endurance.
* Deployment via Docker Compose is mandatory for seamless transition from Ubuntu to Pi 5.
