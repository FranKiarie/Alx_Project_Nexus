# 🎬 Project Nexus: Demo Video Script

**Constraints & Requirements:**
- **Time Limit:** Strictly under 5 minutes (Aim for ~3 mins).
- **Focus:** Show the project in *real-time operation*. Do not talk about unrelated topics.
- **Goal:** Demonstrate functionality AND explain *Industry Best Practices* used.

**Preparation:**
1.  Open your Render URL: [https://project-nexus-vumc.onrender.com/api/docs/](https://project-nexus-vumc.onrender.com/api/docs/)
2.  Open a second tab: [https://project-nexus-vumc.onrender.com/health/](https://project-nexus-vumc.onrender.com/health/)
3.  Have a notepad ready with a unique "Voter ID" (e.g., `demo_user_01`).

---

## 🟢 Scene 1: Introduction & Best Practices (45 seconds)
1.  **Start recording** with the **Swagger UI** on screen.

    > [!TIP]
    > **📸 INSERT SCREENSHOT HERE:** Capture the entire Swagger UI page (`/api/docs/`).

2.  **Voiceover:** "Hi, this is [Your Name] presenting Project Nexus. This is a RESTful Polling API designed with **Industry Best Practices** at its core."
3.  **Action:** Briefly scroll to show the clean API structure.
4.  **Voiceover (The Best Practices Explainer):** "I have integrated several key standards:
    *   **Security:** I use **UUIDs** for all primary keys to prevent enumeration attacks.
    *   **Data Integrity:** Duplicate voting is prevented by strict **Database Constraints**, not just code logic.
    *   **Performance:** All filter fields are indexed (`db_index=True`) for speed.
    *   **Architecture:** The project follows a strictly layered structure (Models, Serializers, Views) for maintainability."

## 🟢 Scene 2: Creating a Poll (Real-Time Demo) (30 seconds)
1.  **Action:** Click **`POST /api/polls/`** -> **Try it out**.
2.  **Input:** Paste this JSON:
    ```json
    {
      "question": "Which backend framework is best?",
      "options": ["Django", "Flask", "FastAPI"]
    }
    ```
3.  **Action:** Click **Execute**.

    > [!TIP]
    > **📸 INSERT SCREENSHOT HERE:** Capture the expanded `POST /api/polls/` section showing the "Execute" button and the Response body.

4.  **Voiceover:** "Here I am creating a poll in real-time. The API validates the input and stores it transactionally."
5.  **Action:** Highlight the **201 Created** status.
6.  **CRITICAL:** **Copy the `id`** (UUID) from the response body.

## 🟢 Scene 3: Voting Successfully (30 seconds)
1.  **Action:** Scroll to **`POST /api/polls/{id}/vote/`** -> **Try it out**.
2.  **Input:**
    *   **id**: Paste the Poll UUID you just copied.
    *   **Body**:
        ```json
        {
          "option_id": "<Copy an option_id from Scene 2 response>",
          "voter_identifier": "judge_01"
        }
        ```
3.  **Action:** Click **Execute**.

    > [!TIP]
    > **📸 INSERT SCREENSHOT HERE:** Capture the expanded `POST /vote/` section with the "201 Created" response visible.

4.  **Action:** Highlight the **201 Created** response (`"Vote recorded successfully"`).
5.  **Voiceover:** "I am casting a vote. The system responds instantly with a success message."

## 🟢 Scene 4: The "Integrity Check" (Showing Best Practices in Action) (30 seconds)
1.  **Action:** **DO NOT CHANGE ANYTHING.** Click **Execute** again immediately.
2.  **Action:** Highlight the **400 Bad Request** error.

    > [!TIP]
    > **📸 INSERT SCREENSHOT HERE:** Capture the "400 Bad Request" error response showing the duplicate vote message.

3.  **Voiceover:** "Now, demonstrating the **Data Integrity** best practice: if I try to vote again, the Database Constraint triggers immediately, rejecting the duplicate. This ensures reliable data."

## 🟢 Scene 5: Checking Results & Deployment (20 seconds)
1.  **Action:** Scroll to **`GET /api/polls/{id}/results/`** -> **Try it out**.
2.  **Input:** Paste the Poll UUID.
3.  **Action:** Click **Execute**.
    
    > [!TIP]
    > **📸 INSERT SCREENSHOT HERE:** Capture the JSON response showing the vote counts.

4.  **Voiceover:** "Finally, fetching aggregated results."
5.  **Action:** Switch tabs to the `/health/` page.

    > [!TIP]
    > **📸 INSERT SCREENSHOT HERE:** Capture the `/health/` endpoint response `{"status": "ok"}`.

6.  **Voiceover:** "The entire system is deployed and live on Render. Thank you."

---

**💾 Save & Upload!**
