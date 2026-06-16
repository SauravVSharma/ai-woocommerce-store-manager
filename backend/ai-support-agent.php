<?php
/*
Plugin Name: AI WooCommerce Store Manager
Description: LangGraph-powered local AI agent for WooCommerce using FastAPI, Ollama, MySQL, and WordPress.
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

    <style>
        .ai-agent-wrap {
            max-width: 780px;
            margin: 30px auto;
            border-radius: 22px;
            overflow: hidden;
            background: #ffffff;
            box-shadow: 0 20px 60px rgba(0,0,0,0.12);
            border: 1px solid #e8e8ef;
            font-family: Inter, Arial, sans-serif;
        }

        .ai-agent-header {
            background: linear-gradient(135deg, #111827, #2563eb);
            color: #fff;
            padding: 24px;
        }

        .ai-agent-header h2 {
            margin: 0;
            font-size: 26px;
            color: #fff;
        }

        .ai-agent-header p {
            margin: 8px 0 0;
            opacity: 0.9;
            font-size: 14px;
        }

        .ai-agent-badges {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 14px;
        }

        .ai-agent-badge {
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.25);
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
        }

        .ai-agent-messages {
            height: 430px;
            overflow-y: auto;
            padding: 22px;
            background: #f8fafc;
        }

        .ai-msg {
            display: flex;
            margin-bottom: 16px;
        }

        .ai-msg.user {
            justify-content: flex-end;
        }

        .ai-bubble {
            max-width: 78%;
            padding: 14px 16px;
            border-radius: 18px;
            line-height: 1.55;
            font-size: 14px;
            white-space: pre-wrap;
        }

        .ai-msg.user .ai-bubble {
            background: #2563eb;
            color: #fff;
            border-bottom-right-radius: 4px;
        }

        .ai-msg.bot .ai-bubble {
            background: #ffffff;
            color: #111827;
            border: 1px solid #e5e7eb;
            border-bottom-left-radius: 4px;
        }

        .ai-agent-suggestions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            padding: 14px 20px;
            background: #fff;
            border-top: 1px solid #eef2f7;
        }

        .ai-suggestion {
            border: 1px solid #dbeafe;
            background: #eff6ff;
            color: #1d4ed8;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 13px;
            cursor: pointer;
            transition: 0.2s;
        }

        .ai-suggestion:hover {
            background: #2563eb;
            color: #fff;
        }

        .ai-agent-input-row {
            display: flex;
            gap: 10px;
            padding: 18px;
            background: #ffffff;
            border-top: 1px solid #e5e7eb;
        }

        .ai-agent-input {
            flex: 1;
            border: 1px solid #d1d5db;
            border-radius: 14px;
            padding: 14px 16px;
            font-size: 15px;
            outline: none;
        }

        .ai-agent-input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.12);
        }

        .ai-agent-send {
            background: #111827;
            color: #fff;
            border: none;
            padding: 0 22px;
            border-radius: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
        }

        .ai-agent-send:hover {
            background: #2563eb;
        }

        .ai-agent-send:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .ai-typing {
            color: #6b7280;
            font-size: 13px;
            padding: 0 22px 14px;
            background: #f8fafc;
            display: none;
        }

        @media(max-width: 640px) {
            .ai-agent-wrap {
                margin: 10px;
                border-radius: 16px;
            }

            .ai-agent-input-row {
                flex-direction: column;
            }

            .ai-agent-send {
                padding: 14px;
            }

            .ai-bubble {
                max-width: 92%;
            }
        }
    </style>

    <div class="ai-agent-wrap">
        <div class="ai-agent-header">
            <h2>AI WooCommerce Store Manager</h2>
            <p>Ask live WooCommerce questions powered by WordPress, FastAPI, LangGraph, Ollama, and MySQL.</p>

            <div class="ai-agent-badges">
                <span class="ai-agent-badge">LangGraph Agent</span>
                <span class="ai-agent-badge">Live Woo Data</span>
                <span class="ai-agent-badge">Local LLM</span>
                <span class="ai-agent-badge">Tool Calling</span>
            </div>
        </div>

        <div id="ai-support-messages" class="ai-agent-messages">
            <div class="ai-msg bot">
                <div class="ai-bubble">
Hi! I can help you analyze your WooCommerce store.

Try asking:
• Show products
• Show low stock products
• Show orders today
• Show pending orders
• Show low stock products and orders today
                </div>
            </div>
        </div>

        <div class="ai-agent-suggestions">
            <button class="ai-suggestion" data-q="show products">Show products</button>
            <button class="ai-suggestion" data-q="show low stock products">Low stock</button>
            <button class="ai-suggestion" data-q="show orders today">Orders today</button>
            <button class="ai-suggestion" data-q="show pending orders">Pending orders</button>
        </div>

        <div id="ai-typing" class="ai-typing">AI is thinking...</div>

        <div class="ai-agent-input-row">
            <input id="ai-support-question" class="ai-agent-input" type="text" placeholder="Ask about products, orders, stock, revenue...">
            <button id="ai-support-send" class="ai-agent-send">Send</button>
        </div>
    </div>

    <script>
    (function () {
        const input = document.getElementById("ai-support-question");
        const messages = document.getElementById("ai-support-messages");
        const sendBtn = document.getElementById("ai-support-send");
        const typing = document.getElementById("ai-typing");

        function escapeHtml(text) {
            const div = document.createElement("div");
            div.textContent = text;
            return div.innerHTML;
        }

        function addMessage(type, text) {
            const row = document.createElement("div");
            row.className = "ai-msg " + type;

            const bubble = document.createElement("div");
            bubble.className = "ai-bubble";
            bubble.innerHTML = escapeHtml(text);

            row.appendChild(bubble);
            messages.appendChild(row);
            messages.scrollTop = messages.scrollHeight;
        }

        async function sendQuestion(questionText = null) {
            const question = questionText || input.value.trim();

            if (!question) {
                return;
            }

            addMessage("user", question);
            input.value = "";
            typing.style.display = "block";
            sendBtn.disabled = true;

            try {
                const response = await fetch("http://127.0.0.1:8010/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        question: question,
                        user_email: "<?php echo esc_js(wp_get_current_user()->user_email ?: 'guest'); ?>"
                    })
                });

                const data = await response.json();

                addMessage("bot", data.answer || "No answer received.");

            } catch (error) {
                addMessage("bot", "Backend not reachable. Please make sure FastAPI is running on port 8010.");
            }

            typing.style.display = "none";
            sendBtn.disabled = false;
            input.focus();
        }

        sendBtn.addEventListener("click", function () {
            sendQuestion();
        });

        input.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                sendQuestion();
            }
        });

        document.querySelectorAll(".ai-suggestion").forEach(function (btn) {
            btn.addEventListener("click", function () {
                sendQuestion(btn.getAttribute("data-q"));
            });
        });
    })();
    </script>

    <?php
    return ob_get_clean();
}
