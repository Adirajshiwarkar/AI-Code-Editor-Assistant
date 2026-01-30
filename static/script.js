document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const fileInput = document.getElementById('file-input');
    const fileStatus = document.getElementById('file-status');
    const pasteBtn = document.getElementById('paste-btn');

    // Sidebar
    const navItems = document.querySelectorAll('.nav-item');
    const pasteModal = document.getElementById('paste-modal');
    const pasteArea = document.getElementById('paste-area');
    const confirmPaste = document.getElementById('confirm-paste');
    const cancelPaste = document.getElementById('cancel-paste');

    // Code Section
    const codeSection = document.getElementById('code-editor-section');
    const codeDisplay = document.querySelector('#code-display code');
    const closeCodeBtn = document.getElementById('close-code-btn');
    const copyCodeBtn = document.getElementById('copy-code-btn');

    let selectedFile = null;
    let pastedCode = null;
    let chatHistory = []; // Stores the last 10 messages

    // --- Helper Functions ---

    function appendMessage(role, content, isHtml = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;

        const bubble = document.createElement('div');
        bubble.className = 'bubble';

        if (isHtml) {
            bubble.innerHTML = content;
        } else {
            // Simple markdown-like formatting for code blocks and bold text
            let processed = content
                .replace(/```([\s\S]*?)```/g, '<pre class="inline-code"><code>$1</code></pre>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\n/g, '<br>');
            bubble.innerHTML = processed;
        }

        msgDiv.appendChild(bubble);
        chatContainer.appendChild(msgDiv);

        // Smooth scroll to bottom
        setTimeout(() => {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);

        return msgDiv;
    }

    function showCode(code) {
        if (!code) return;
        codeDisplay.textContent = code;
        codeSection.style.display = 'flex';
        // Trigger animation
        setTimeout(() => {
            codeSection.style.opacity = '1';
            codeSection.style.transform = 'translateX(0)';
        }, 10);
    }

    async function processRequest() {
        const instruction = userInput.value.trim();
        if (!instruction && !selectedFile && !pastedCode) return;

        const formData = new FormData();
        formData.append('instruction', instruction || 'Analyze this code');
        formData.append('history', JSON.stringify(chatHistory));

        if (selectedFile) {
            formData.append('file', selectedFile);
        } else if (pastedCode) {
            formData.append('code_content', pastedCode);
        }

        appendMessage('user', instruction || "[Analyzing Code Content]");

        // Add to history
        chatHistory.push({ role: 'user', content: instruction || "[Code Analysis Request]" });
        if (chatHistory.length > 10) chatHistory.shift();

        userInput.value = '';
        userInput.style.height = '24px'; // Reset height

        sendBtn.disabled = true;
        sendBtn.style.opacity = '0.5';

        const loadingMsg = appendMessage('assistant', '<div class="typing-indicator"><span></span><span></span><span></span></div> Thinking...', true);
        let assistantBubble = null;
        let reportContent = "";

        try {
            const response = await fetch('/api/stream', {
                method: 'POST',
                body: formData
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));

                            if (data.error) {
                                if (loadingMsg) loadingMsg.remove();
                                appendMessage('assistant', `<span style="color: var(--error)"><strong>Error:</strong> ${data.error}</span>`, true);
                                continue;
                            }

                            const content = data.content;

                            if (content.startsWith('[STEP]')) {
                                const stepText = content.slice(6).trim();
                                if (loadingMsg) {
                                    loadingMsg.querySelector('.bubble').innerHTML = `<div class="typing-indicator"><span></span><span></span><span></span></div> ${stepText}...`;
                                }
                            } else if (content.startsWith('[START_REPORT]')) {
                                if (loadingMsg) loadingMsg.remove();
                                assistantBubble = appendMessage('assistant', '', true);
                            } else if (content.includes('[FINAL_CODE]')) {
                                const [reportPart, codePart] = content.split('[FINAL_CODE]');
                                if (reportPart && assistantBubble) {
                                    reportContent += reportPart;
                                    updateBubble(assistantBubble, reportContent);
                                }
                                if (codePart) {
                                    showCode(codePart.trim());
                                }
                            } else if (assistantBubble) {
                                reportContent += content;
                                updateBubble(assistantBubble, reportContent);
                            }
                        } catch (e) {
                            console.error("Error parsing stream chunk", e);
                        }
                    }
                }
            }

            // Store final report in history
            if (reportContent) {
                chatHistory.push({ role: 'assistant', content: reportContent });
                if (chatHistory.length > 10) chatHistory.shift();
            }

        } catch (error) {
            if (loadingMsg) loadingMsg.remove();
            appendMessage('assistant', `<span style="color: var(--error)"><strong>Connection Error:</strong> Could not reach the reasoning engine.</span>`, true);
        } finally {
            sendBtn.disabled = false;
            sendBtn.style.opacity = '1';
            selectedFile = null;
            pastedCode = null;
            fileStatus.innerText = '';
        }
    }

    function updateBubble(bubble, content) {
        const bubbleInner = bubble.querySelector('.bubble');
        let processed = content
            .replace(/```([\s\S]*?)```/g, '<pre class="inline-code"><code>$1</code></pre>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
        bubbleInner.innerHTML = processed;

        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'auto'
        });
    }

    // --- Event Listeners ---

    sendBtn.addEventListener('click', processRequest);

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            processRequest();
        }
    });

    // Auto-resize textarea
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.scrollHeight > 200) {
            this.style.overflowY = 'scroll';
            this.style.height = '200px';
        } else {
            this.style.overflowY = 'hidden';
        }
    });

    uploadBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            selectedFile = e.target.files[0];
            pastedCode = null;
            fileStatus.innerText = `attached: ${selectedFile.name}`;
            appendMessage('assistant', `File **${selectedFile.name}** has been uploaded. What is your directive?`);
        }
    });

    pasteBtn.addEventListener('click', () => {
        pasteModal.style.display = 'flex';
        pasteArea.focus();
    });

    cancelPaste.addEventListener('click', () => {
        pasteModal.style.display = 'none';
        pasteArea.value = '';
    });

    confirmPaste.addEventListener('click', () => {
        const content = pasteArea.value.trim();
        if (content) {
            pastedCode = content;
            selectedFile = null;
            fileStatus.innerText = "snippet injected";
            pasteModal.style.display = 'none';
            pasteArea.value = '';
            appendMessage('assistant', "Code snippet injected into the buffer. Ready for instruction.");
        }
    });

    closeCodeBtn.addEventListener('click', () => {
        codeSection.style.opacity = '0';
        codeSection.style.transform = 'translateX(20px)';
        setTimeout(() => {
            codeSection.style.display = 'none';
        }, 500);
    });

    copyCodeBtn.addEventListener('click', () => {
        const code = codeDisplay.textContent;
        navigator.clipboard.writeText(code).then(() => {
            const originalText = copyCodeBtn.innerHTML;
            copyCodeBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            copyCodeBtn.classList.add('success');
            setTimeout(() => {
                copyCodeBtn.innerHTML = originalText;
                copyCodeBtn.classList.remove('success');
            }, 2000);
        });
    });

    // --- Sidebar Navigation ---
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const view = item.getAttribute('data-view');

            // Update UI state
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            if (view === 'assistant') {
                // Return to chat
                appendMessage('assistant', "Returning to the main assistant view. How can I help with your code?");
            } else {
                // Show "Coming Soon" for other views
                const viewName = view.charAt(0).toUpperCase() + view.slice(1);
                appendMessage('assistant', `The **${viewName}** module is being initialized. For now, you can continue using the Assistant for code review and breakdown.`, true);

                // Add a cool visual effect to simulate loading
                const loadingBubble = appendMessage('assistant', `<div class="typing-indicator"><span></span><span></span><span></span></div> Synchronizing ${viewName} data...`, true);
                setTimeout(() => {
                    loadingBubble.innerHTML = `<i class="fas fa-info-circle"></i> ${viewName} interface is currently in read-only mode for this session.`;
                }, 1500);
            }
        });
    });
});
