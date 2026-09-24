// Create chat widget UI dynamically
const chatWidget = document.createElement('div');
chatWidget.innerHTML = `
    <div id="chat-box" style="position: fixed; bottom: 20px; right: 20px; width: 300px; background: white; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); display: none; flex-direction: column; z-index: 1000;">
        <div style="background: var(--primary-blue); color: white; padding: 10px; border-radius: 8px 8px 0 0; font-weight: bold;">WordbitX AI</div>
        <div id="chat-messages" style="height: 250px; overflow-y: auto; padding: 10px; font-size: 0.9rem; display: flex; flex-direction: column; gap: 8px;"></div>
        <input type="text" id="chat-input" placeholder="Type a message..." style="padding: 10px; border: none; border-top: 1px solid #ddd; outline: none; border-radius: 0 0 8px 8px;">
    </div>
    <button id="chat-toggle" style="position: fixed; bottom: 20px; right: 20px; background: var(--primary-green); color: white; border: none; border-radius: 50%; width: 50px; height: 50px; font-size: 1.5rem; cursor: pointer; z-index: 1001;">💬</button>
`;
document.body.appendChild(chatWidget);

const chatBox = document.getElementById('chat-box');
const chatToggle = document.getElementById('chat-toggle');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

// Toggle chat window visibility
chatToggle.addEventListener('click', () => {
    chatBox.style.display = chatBox.style.display === 'none' ? 'flex' : 'none';
});

// Handle sending messages to backend API
chatInput.addEventListener('keypress', async (e) => {
    if (e.key === 'Enter' && chatInput.value.trim() !== '') {
        const userMsg = chatInput.value;

        // Show user message
        chatMessages.innerHTML += `<div style="align-self: flex-end; background: #E5E7EB; padding: 8px; border-radius: 5px;">${userMsg}</div>`;
        chatInput.value = '';

        try {
            // Fetch AI response from routes.py
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg })
            });
            const data = await response.json();

            // Show AI reply
            chatMessages.innerHTML += `<div style="align-self: flex-start; background: var(--primary-green); color: white; padding: 8px; border-radius: 5px;">${data.reply}</div>`;
        } catch (error) {
            chatMessages.innerHTML += `<div style="color: red; font-size: 0.8rem;">Error connecting to AI.</div>`;
        }

        // Auto-scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});