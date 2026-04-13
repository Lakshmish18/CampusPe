/*
  filename: js/chat.js
  description: jQuery chat interactions for message flow, formatting, typewriter replies, theme, export, and mobile sidebar behavior.
*/

$(document).ready(function () {
  // ========================
  // Data Sources
  // ========================
  const aiResponseOptions = [
    "Okay, I'm ready to assist you with any task or question you may have! Feel free to ask me about writing, analysis, math, coding, general knowledge, or any other topic, and I'll do my best to provide a thorough and helpful response.",
    "That's a great question! Here's what I know about that topic...",
    "I'd be happy to help with that. Let me break it down for you step by step.",
    "Sure! Here's a clear explanation: The concept works by...",
    "Great choice! Here are some tips and best practices for that...",
    "I can definitely help with that. Based on what you've shared, I'd suggest...",
    "Interesting question! There are a few different perspectives on this...",
    "Absolutely! Here's a concise and accurate answer to your question..."
  ];
  let hasSentFirstMessage = false;

  // ========================
  // Utility Functions
  // ========================

  // Returns a compact localized timestamp displayed on each message.
  function getCurrentMessageTime() {
    return new Date().toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit"
    });
  }

  // Keeps the textarea at one line when cleared.
  function resetInputToSingleLine() {
    const inputElement = document.getElementById("user-input");
    if (!inputElement) return;
    inputElement.style.height = "auto";
    inputElement.style.height = "24px";
  }

  // Auto-resizes input to content height while capping growth.
  function resizeInputToContent() {
    const inputElement = document.getElementById("user-input");
    if (!inputElement) return;
    inputElement.style.height = "auto";
    inputElement.style.height = Math.min(inputElement.scrollHeight, 120) + "px";
  }

  // Enables or disables send button based on trimmed input.
  function syncSendButtonState() {
    const trimmedInput = ($("#user-input").val() || "").trim();
    $("#send-btn").prop("disabled", trimmedInput === "");
  }

  // Converts lightweight markdown text into styled HTML snippets.
  function formatMessageContent(rawText) {
    let formattedText = rawText;
    formattedText = formattedText.replace(/```(\w*)\n?([\s\S]*?)```/g, function (fullMatch, languageLabel, codeText) {
      return '<div class="code-block"><div class="code-header"><span>' + (languageLabel || "code") + '</span><button class="copy-code-btn">Copy</button></div><pre><code>' + codeText.trim() + "</code></pre></div>";
    });
    formattedText = formattedText.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    formattedText = formattedText.replace(/\*(.*?)\*/g, "<em>$1</em>");
    return formattedText;
  }

  // Smooth-scrolls the messages container to latest content.
  function scrollToBottom() {
    try {
      const messagesContainer = document.getElementById("messages-container");
      if (!messagesContainer) return;
      $(messagesContainer).stop(true).animate({ scrollTop: messagesContainer.scrollHeight }, 200);
    } catch (scrollError) {
      // Intentionally ignored to prevent UI-breaking runtime exceptions.
    }
  }

  // Shows transient typing UI while mock AI response is pending.
  function showTypingIndicator() {
    $("#typing-indicator").removeClass("hidden");
    scrollToBottom();
  }

  // Hides typing UI after response has completed.
  function hideTypingIndicator() {
    $("#typing-indicator").addClass("hidden");
  }

  // Hides welcome card once first message is sent.
  function hideWelcomeScreenAfterFirstMessage() {
    if (!hasSentFirstMessage) {
      hasSentFirstMessage = true;
      $("#welcome-screen").stop(true, true).fadeOut(200);
    }
  }

  // Renders a complete message block for user or AI.
  function addMessage(messageText, senderType) {
    const isAiSender = senderType === "ai";
    const avatarClassName = isAiSender ? "ai-avatar" : "user-avatar";
    const avatarMarkup = isAiSender ? '<i class="fa-solid fa-bolt"></i>' : "U";
    const displayName = isAiSender ? "Claude" : "You";
    const formattedText = formatMessageContent(messageText);
    const actionRowMarkup = isAiSender
      ? '<div class="msg-actions"><i class="fa-regular fa-thumbs-up" title="Like"></i><i class="fa-regular fa-thumbs-down" title="Dislike"></i><i class="fa-regular fa-copy" title="Copy"></i><i class="fa-solid fa-rotate-right" title="Retry"></i><i class="fa-regular fa-flag" title="Report"></i><span class="msg-meta">0 Likes &nbsp;|&nbsp; Policy</span></div>'
      : "";
    const messageMarkup = '<div class="message ' + senderType + '-message"><div class="msg-header"><div class="msg-avatar ' + avatarClassName + '">' + avatarMarkup + '</div><span class="msg-name">' + displayName + '</span><span class="msg-time">' + getCurrentMessageTime() + '</span></div><div class="msg-bubble">' + formattedText + "</div>" + actionRowMarkup + "</div>";
    $("#messages-wrapper").append(messageMarkup);
    scrollToBottom();
  }

  // Renders AI response with character-by-character animation then applies full formatting.
  function typewriteMessage(fullMessageText) {
    const messageMarkup = '<div class="message ai-message"><div class="msg-header"><div class="msg-avatar ai-avatar"><i class="fa-solid fa-bolt"></i></div><span class="msg-name">Claude</span><span class="msg-time">' + getCurrentMessageTime() + '</span></div><div class="msg-bubble"></div><div class="msg-actions"><i class="fa-regular fa-thumbs-up" title="Like"></i><i class="fa-regular fa-thumbs-down" title="Dislike"></i><i class="fa-regular fa-copy" title="Copy"></i><i class="fa-solid fa-rotate-right" title="Retry"></i><i class="fa-regular fa-flag" title="Report"></i><span class="msg-meta">0 Likes &nbsp;|&nbsp; Policy</span></div></div>';
    $("#messages-wrapper").append(messageMarkup);
    const currentMessageBubble = $("#messages-wrapper .message:last-child .msg-bubble");
    let characterIndex = 0;
    const typingIntervalId = setInterval(function () {
      characterIndex += 1;
      currentMessageBubble.text(fullMessageText.slice(0, characterIndex));
      scrollToBottom();
      if (characterIndex >= fullMessageText.length) {
        clearInterval(typingIntervalId);
        currentMessageBubble.html(formatMessageContent(fullMessageText));
      }
    }, 18);
  }

  // Sends user message, prevents blank sends, resets textarea, and triggers mock AI response.
  function sendMessage(rawInputMessage) {
    const trimmedMessage = (rawInputMessage || "").trim();
    if (!trimmedMessage) return;
    addMessage(trimmedMessage, "user");
    hideWelcomeScreenAfterFirstMessage();
    $("#user-input").val("");
    resetInputToSingleLine();
    syncSendButtonState();
    setTimeout(function () {
      showTypingIndicator();
      const responseDelay = Math.floor(Math.random() * 1000) + 1000;
      setTimeout(function () {
        hideTypingIndicator();
        const randomIndex = Math.floor(Math.random() * aiResponseOptions.length);
        const aiResponseText = aiResponseOptions[randomIndex];
        typewriteMessage(aiResponseText);
      }, responseDelay);
    }, 300);
  }

  // Resets chat state and restores welcome screen for a brand new conversation.
  function startNewChat() {
    $("#messages-wrapper").empty();
    $("#typing-indicator").addClass("hidden");
    $("#welcome-screen").stop(true, true).fadeIn(250);
    hasSentFirstMessage = false;
    $("#user-input").val("");
    resetInputToSingleLine();
    syncSendButtonState();
  }

  // ========================
  // Event Bindings
  // ========================

  // Initializes default controls state on page load.
  function initializeInterfaceState() {
    $("#send-btn").prop("disabled", true);
    resetInputToSingleLine();
    hideTypingIndicator();
  }

  // Updates composer state as the user types.
  $("#user-input").on("input", function () {
    resizeInputToContent();
    syncSendButtonState();
  });

  // Sends on Enter, allows newline on Shift+Enter.
  $("#user-input").on("keydown", function (keyboardEvent) {
    if (keyboardEvent.key === "Enter" && !keyboardEvent.shiftKey) {
      keyboardEvent.preventDefault();
      sendMessage($(this).val());
    }
  });

  // Sends using the send button.
  $("#send-btn").on("click", function () {
    sendMessage($("#user-input").val());
  });

  // Sends predefined prompts from suggestion cards.
  $(document).on("click", ".suggestion-card", function () {
    const selectedPrompt = String($(this).data("prompt") || "");
    $("#user-input").val(selectedPrompt);
    sendMessage(selectedPrompt);
  });

  // Clears conversation and restores initial UI.
  $("#new-chat-btn, #new-chat-mobile").on("click", function () {
    startNewChat();
  });

  // Copies the text of a rendered chat message.
  $(document).on("click", ".fa-copy", function () {
    try {
      const bubbleText = $(this).closest(".message").find(".msg-bubble").text();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(bubbleText);
      }
      $(this).removeClass("fa-regular fa-copy").addClass("fa-solid fa-check");
      const copiedIcon = this;
      setTimeout(function () {
        $(copiedIcon).removeClass("fa-solid fa-check").addClass("fa-regular fa-copy");
      }, 1500);
    } catch (copyError) {
      // Clipboard may be unavailable in insecure contexts.
    }
  });

  // Copies code from generated code blocks.
  $(document).on("click", ".copy-code-btn", function () {
    try {
      const copyButton = $(this);
      const codeBlockText = copyButton.closest(".code-block").find("pre code").text();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(codeBlockText);
      }
      copyButton.text("Copied");
      setTimeout(function () {
        copyButton.text("Copy");
      }, 1200);
    } catch (copyCodeError) {
      // Silent fallback keeps UI responsive even if clipboard fails.
    }
  });

  // Handles mobile sidebar drawer toggle.
  $("#hamburger-btn").on("click", function () {
    $("#sidebar").toggleClass("sidebar-open");
    $("#sidebar-overlay").toggleClass("visible");
  });

  // Closes sidebar when tapping outside overlay.
  $("#sidebar-overlay").on("click", function () {
    $("#sidebar").removeClass("sidebar-open");
    $(this).removeClass("visible");
  });

  // Switches between light and dark theme variables.
  $("#theme-toggle").on("click", function () {
    const isDarkThemeActive = $("html").attr("data-theme") === "dark";
    $("html").attr("data-theme", isDarkThemeActive ? "" : "dark");
    $(this).find("i").toggleClass("fa-moon fa-sun");
  });

  // Updates active chat history selection in sidebar.
  $(document).on("click", ".history-item", function () {
    $(".history-item").removeClass("active");
    $(this).addClass("active");
  });

  // Ensures export button exists in topbar actions.
  if (!$("#export-chat-btn").length) {
    const exportButtonMarkup = '<button id="export-chat-btn" class="icon-btn" type="button" aria-label="Export chat"><i class="fa-solid fa-file-arrow-down"></i></button>';
    $(".chat-topbar .topbar-actions").first().append(exportButtonMarkup);
  }

  // Exports visible chat log as text file.
  $(document).on("click", "#export-chat-btn", function () {
    try {
      let exportedContent = "";
      $("#messages-wrapper .message").each(function () {
        const senderName = $(this).find(".msg-name").text();
        const messageText = $(this).find(".msg-bubble").text();
        const messageTime = $(this).find(".msg-time").text();
        exportedContent += "[" + messageTime + "] " + senderName + ": " + messageText + "\n\n";
      });
      const exportBlob = new Blob([exportedContent], { type: "text/plain" });
      const downloadAnchor = document.createElement("a");
      downloadAnchor.href = URL.createObjectURL(exportBlob);
      downloadAnchor.download = "chat-export-" + Date.now() + ".txt";
      downloadAnchor.click();
    } catch (exportError) {
      // Safe fail in case browser blocks downloads.
    }
  });

  // Final startup setup.
  initializeInterfaceState();
});
