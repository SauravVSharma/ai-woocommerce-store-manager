<?php
/*
Plugin Name: AI Support Agent
Description: Local WordPress AI support agent connected with FastAPI backend.
Version: 1.0
Author: Saurav Sharma
*/

if (!defined('ABSPATH')) {
    exit;
}

add_shortcode('ai_support_agent', 'ai_support_agent_ui');

function ai_support_agent_ui() {
    ob_start();
    ?>

    <div id="ai-support-agent" style="max-width:600px;border:1px solid #ddd;padding:15px;border-radius:8px;">
        <h3>AI Support Agent</h3>

        <div id="ai-support-messages" style="height:300px;overflow:auto;border:1px solid #eee;padding:10px;margin-bottom:10px;background:#fafafa;"></div>

        <input id="ai-support-question" type="text" placeholder="Ask support question..." style="width:100%;padding:10px;margin-bottom:10px;">

        <button id="ai-support-send" style="padding:10px 15px;cursor:pointer;">
            Send
        </button>
    </div>

    <script>
    document.getElementById("ai-support-send").addEventListener("click", async function () {
        const input = document.getElementById("ai-support-question");
        const messages = document.getElementById("ai-support-messages");

        const question = input.value.trim();

        if (!question) {
            return;
        }

        messages.innerHTML += "<p><strong>You:</strong> " + question + "</p>";

        input.value = "";

        try {
            const response = await fetch("http://127.0.0.1:8010/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question,
                    user_email: "<?php echo esc_js(wp_get_current_user()->user_email); ?>"
                })
            });

            const data = await response.json();

            messages.innerHTML += "<p><strong>AI:</strong> " + data.answer + "</p>";

        } catch (error) {
            messages.innerHTML += "<p><strong>Error:</strong> Backend not reachable.</p>";
        }

        messages.scrollTop = messages.scrollHeight;
    });
    </script>

    <?php
    return ob_get_clean();
}
