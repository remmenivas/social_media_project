
"use strict";

const API = "";
let allUsers = [];
let allPosts = [];
let currentChatTimer = null;
let toastTimer = null;

const $ = (id) => document.getElementById(id);

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

function safeImageURL(value) {
    try {
        const url = new URL(String(value || ""));
        return ["http:", "https:"].includes(url.protocol) ? url.href : "";
    } catch {
        return "";
    }
}

function getCurrentUserId() {
    return $("user")?.value || "";
}

function getUserById(id) {
    return allUsers.find(user => String(user.user_id) === String(id));
}

function displayName(user) {
    return user?.full_name || user?.username || "Community member";
}

function initials(name) {
    return String(name || "U").trim().charAt(0).toUpperCase() || "U";
}

function formatDate(value) {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value);
    return date.toLocaleString([], {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit"
    });
}

function showToast(message) {
    const toast = $("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
}

async function apiJSON(url, options = {}) {
    const response = await fetch(API + url, {
        ...options,
        headers: {
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...(options.headers || {})
        }
    });

    const text = await response.text();
    let data = {};

    if (text) {
        try {
            data = JSON.parse(text);
        } catch {
            data = { message: text };
        }
    }

    if (!response.ok) {
        throw new Error(data.error || data.message || `Request failed (${response.status})`);
    }

    return data;
}

function jsonOptions(method, data) {
    return {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    };
}

/* Screen navigation */

function setActiveNavigation(screen) {
    $("homeNav")?.classList.toggle("active", screen === "home");
    $("messagesNav")?.classList.toggle("active", screen === "messages");
}

function showHome() {
    $("feedPage").hidden = false;
    $("messagesPage").hidden = true;
    setActiveNavigation("home");

    if (currentChatTimer) {
        clearInterval(currentChatTimer);
        currentChatTimer = null;
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
}

function openMessagesPage() {
    $("feedPage").hidden = true;
    $("messagesPage").hidden = false;
    setActiveNavigation("messages");

    renderConversationList();
    loadMessages();

    if (currentChatTimer) clearInterval(currentChatTimer);
    currentChatTimer = setInterval(() => {
        if (!$("messagesPage").hidden && $("chatUser").value) {
            loadMessages(true);
        }
    }, 5000);

    window.scrollTo({ top: 0, behavior: "smooth" });
}

window.showHome = showHome;
window.openMessagesPage = openMessagesPage;

/* Users and profiles */

async function loadUsers() {
    try {
        const data = await apiJSON("/api/users");
        allUsers = Array.isArray(data) ? data : (data.users || []);

        const postUser = $("user");
        const profileUser = $("profileUser");
        const chatUser = $("chatUser");

        postUser.innerHTML = '<option value="">Choose a user</option>';
        profileUser.innerHTML = '<option value="">Select a user</option>';
        chatUser.innerHTML = '<option value="">Select a person</option>';

        allUsers.forEach(user => {
            const name = `${displayName(user)} (@${user.username || "user"})`;

            postUser.add(new Option(name, user.user_id));
            profileUser.add(new Option(name, user.user_id));

            if (String(user.user_id) !== String(getCurrentUserId())) {
                chatUser.add(new Option(name, user.user_id));
            }
        });

        renderConversationList();
    } catch (error) {
        showToast("Could not load users: " + error.message);
        $("conversationList").innerHTML =
            '<div class="empty-state">Could not load community members.</div>';
    }
}

async function viewProfile() {
    const id = $("profileUser").value;
    if (!id) {
        showToast("Please select a user first.");
        return;
    }

    try {
        const data = await apiJSON(`/api/users/${encodeURIComponent(id)}`);
        const user = data.user || data;
        const name = displayName(user);
        const bio = user.bio || "This member hasn't added a bio yet.";
        const count = user.post_count ?? user.posts_count ?? 0;
        const image = safeImageURL(user.profile_image_url);

        $("profileDetails").innerHTML = `
            <div class="profile-card">
                ${image
                    ? `<img class="avatar" src="${escapeHTML(image)}" alt="" style="object-fit:cover">`
                    : `<div class="avatar">${escapeHTML(initials(name))}</div>`}
                <h3>${escapeHTML(name)}</h3>
                <p class="muted">@${escapeHTML(user.username || "user")}</p>
                <p>${escapeHTML(bio)}</p>
                <div class="profile-stats">
                    <span><strong>${escapeHTML(count)}</strong> posts</span>
                    <span><strong>${escapeHTML(user.email || "—")}</strong></span>
                </div>
                <button class="secondary-button" onclick="startConversation('${escapeHTML(user.user_id)}')">
                    Message user →
                </button>
            </div>`;
    } catch (error) {
        showToast("Could not load profile: " + error.message);
    }
}

window.viewProfile = viewProfile;

function startConversation(userId) {
    const chatUser = $("chatUser");
    const option = [...chatUser.options].find(item => item.value === String(userId));

    if (!option) {
        showToast("You cannot start a conversation with this account.");
        return;
    }

    chatUser.value = String(userId);
    chatUser.dispatchEvent(new Event("change"));
    openMessagesPage();
}

window.startConversation = startConversation;

/* Conversation list */

function renderConversationList(filter = "") {
    const container = $("conversationList");
    if (!container) return;

    const currentUserId = getCurrentUserId();
    const query = filter.trim().toLowerCase();

    const users = allUsers.filter(user => {
        if (String(user.user_id) === String(currentUserId)) return false;
        const name = displayName(user).toLowerCase();
        const username = String(user.username || "").toLowerCase();
        return name.includes(query) || username.includes(query);
    });

    $("conversationCount").textContent = String(users.length);

    if (!users.length) {
        container.innerHTML = '<div class="empty-state">No people found.</div>';
        return;
    }

    const selectedId = $("chatUser").value;

    container.innerHTML = users.map(user => {
        const name = displayName(user);
        const active = String(user.user_id) === String(selectedId);
        const image = safeImageURL(user.profile_image_url);

        return `
            <button type="button"
                class="conversation-item ${active ? "active" : ""}"
                data-user-id="${escapeHTML(user.user_id)}">
                ${image
                    ? `<img class="avatar" src="${escapeHTML(image)}" alt=""
                           style="object-fit:cover">`
                    : `<span class="avatar">${escapeHTML(initials(name))}</span>`}
                <span class="conversation-person">
                    <strong>${escapeHTML(name)}</strong>
                    <small>@${escapeHTML(user.username || "member")}</small>
                </span>
            </button>`;
    }).join("");

    container.querySelectorAll("[data-user-id]").forEach(button => {
        button.addEventListener("click", () => {
            $("chatUser").value = button.dataset.userId;
            $("chatUser").dispatchEvent(new Event("change"));
        });
    });
}

function filterConversations() {
    renderConversationList($("conversationSearch").value);
}

window.filterConversations = filterConversations;

$("chatUser").addEventListener("change", () => {
    const id = $("chatUser").value;
    const user = getUserById(id);

    renderConversationList($("conversationSearch").value);

    if (!user) {
        $("activeChat").hidden = true;
        $("chatWelcome").hidden = false;
        return;
    }

    $("chatWelcome").hidden = true;
    $("activeChat").hidden = false;
    $("chatPersonName").textContent = displayName(user);
    $("chatAvatar").textContent = initials(displayName(user));
    $("chatInput").focus();

    loadMessages();
});

/* Posts */

async function loadPosts(search = "") {
    const postsContainer = $("posts");
    postsContainer.innerHTML = '<div class="empty-state">Loading posts...</div>';

    try {
        const query = search.trim()
            ? `?search=${encodeURIComponent(search.trim())}`
            : "";

        const data = await apiJSON("/api/posts" + query);
        allPosts = Array.isArray(data) ? data : (data.posts || []);

        if (!allPosts.length) {
            postsContainer.innerHTML =
                '<div class="empty-state">No posts yet. Be the first to share something!</div>';
            return;
        }

        postsContainer.innerHTML = allPosts.map(post => {
            const name = post.full_name || post.username || "Community member";
            const image = safeImageURL(post.image_url);
            const postId = escapeHTML(post.post_id);
            const likes = Number(post.likes ?? post.like_count ?? 0);
            const isOwner = String(post.user_id) === String(getCurrentUserId());

            return `
                <article class="post-card" id="post-${postId}">
                    <div class="post-top">
                        <div class="avatar">${escapeHTML(initials(name))}</div>
                        <div class="post-author">
                            <strong>${escapeHTML(name)}</strong>
                            <small>@${escapeHTML(post.username || "member")} ·
                                ${escapeHTML(formatDate(post.created_at))}</small>
                        </div>
                    </div>

                    <div class="post-content">${escapeHTML(post.content || "")}</div>

                    ${image
                        ? `<img class="post-image" src="${escapeHTML(image)}"
                                alt="Post image" loading="lazy"
                                onerror="this.style.display='none'">`
                        : ""}

                    <div class="post-actions">
                        <button class="action-button"
                            onclick="likePost('${postId}')">♡ Like (${likes})</button>
                        <button class="action-button"
                            onclick="unlikePost('${postId}')">♥ Unlike</button>
                        <button class="action-button"
                            onclick="toggleComments('${postId}')">▤ Comments</button>
                        ${isOwner
                            ? `<button class="action-button danger"
                                  onclick="deletePost('${postId}')">Delete</button>`
                            : ""}
                    </div>

                    <div class="comment-area" id="comments-${postId}" hidden>
                        <div class="comment-list" id="comment-list-${postId}">
                            <div class="muted small-text">Load comments to see the discussion.</div>
                        </div>
                        <form class="comment-form"
                            onsubmit="addComment(event, '${postId}'); return false;">
                            <input class="field" id="comment-input-${postId}"
                                   maxlength="2000" placeholder="Write a comment..." required>
                            <button class="secondary-button" type="submit">Send</button>
                        </form>
                    </div>
                </article>`;
        }).join("");
    } catch (error) {
        postsContainer.innerHTML =
            `<div class="empty-state">Could not load posts.<br>${escapeHTML(error.message)}</div>`;
    }
}

function searchPosts() {
    loadPosts($("searchInput").value);
}

window.searchPosts = searchPosts;

async function createPost() {
    const userId = getCurrentUserId();
    const content = $("content").value.trim();
    const imageUrl = $("image_url").value.trim();

    if (!userId) {
        showToast("Please select a user.");
        return;
    }
    if (!content) {
        showToast("Please write something before publishing.");
        return;
    }

    const button = document.querySelector("#create .primary-button");
    if (button) button.disabled = true;

    try {
        await apiJSON("/api/posts", jsonOptions("POST", {
            user_id: Number(userId),
            content,
            image_url: imageUrl || null
        }));

        $("content").value = "";
        $("image_url").value = "";
        showToast("Your post has been published!");
        await loadPosts($("searchInput").value);
    } catch (error) {
        showToast("Could not publish: " + error.message);
    } finally {
        if (button) button.disabled = false;
    }
}

window.createPost = createPost;

async function likePost(postId) {
    const userId = getCurrentUserId();
    if (!userId) {
        showToast("Select a user before liking a post.");
        return;
    }

    try {
        await apiJSON(`/api/posts/${encodeURIComponent(postId)}/like`,
            jsonOptions("POST", { user_id: Number(userId) }));
        await loadPosts($("searchInput").value);
    } catch (error) {
        showToast("Could not like post: " + error.message);
    }
}

async function unlikePost(postId) {
    const userId = getCurrentUserId();
    if (!userId) {
        showToast("Select a user first.");
        return;
    }

    try {
        await apiJSON(`/api/posts/${encodeURIComponent(postId)}/unlike`,
            jsonOptions("POST", { user_id: Number(userId) }));
        await loadPosts($("searchInput").value);
    } catch (error) {
        showToast("Could not unlike post: " + error.message);
    }
}

async function deletePost(postId) {
    if (!confirm("Are you sure you want to delete this post?")) return;

    try {
        await apiJSON(`/api/posts/${encodeURIComponent(postId)}`, {
            method: "DELETE"
        });
        showToast("Post deleted.");
        await loadPosts($("searchInput").value);
    } catch (error) {
        showToast("Could not delete post: " + error.message);
    }
}

window.likePost = likePost;
window.unlikePost = unlikePost;
window.deletePost = deletePost;

/* Comments */

async function toggleComments(postId) {
    const section = $(`comments-${postId}`);
    section.hidden = !section.hidden;
    if (!section.hidden) await loadComments(postId);
}

async function loadComments(postId) {
    const list = $(`comment-list-${postId}`);
    list.innerHTML = '<div class="muted small-text">Loading comments...</div>';

    try {
        const data = await apiJSON(`/api/posts/${encodeURIComponent(postId)}/comments`);
        const comments = Array.isArray(data) ? data : (data.comments || []);

        list.innerHTML = comments.length ? comments.map(comment => `
            <div class="comment-item">
                <strong>${escapeHTML(comment.full_name || comment.username || "Member")}</strong>
                <span>${escapeHTML(comment.comment_text || comment.content || "")}</span>
            </div>`).join("") :
            '<div class="muted small-text">No comments yet. Start the conversation!</div>';
    } catch (error) {
        list.innerHTML = `<div class="muted small-text">${escapeHTML(error.message)}</div>`;
    }
}

async function addComment(event, postId) {
    event.preventDefault();

    const userId = getCurrentUserId();
    const input = $(`comment-input-${postId}`);
    const commentText = input.value.trim();

    if (!userId || !commentText) {
        showToast("Select a user and enter a comment.");
        return;
    }

    try {
        await apiJSON(`/api/posts/${encodeURIComponent(postId)}/comments`,
            jsonOptions("POST", {
                user_id: Number(userId),
                comment_text: commentText
            }));

        input.value = "";
        await loadComments(postId);
        showToast("Comment added.");
    } catch (error) {
        showToast("Could not add comment: " + error.message);
    }
}

window.toggleComments = toggleComments;
window.addComment = addComment;

/* Messages */

async function loadMessages(silent = false) {
    const recipientId = $("chatUser").value;
    const senderId = getCurrentUserId();

    if (!recipientId || !senderId || recipientId === senderId) return;

    const container = $("chatMessages");

    try {
        const params = new URLSearchParams({
            user1_id: senderId,
            user2_id: recipientId
        });

        const data = await apiJSON(`/api/messages?${params.toString()}`);
        const messages = Array.isArray(data) ? data : (data.messages || []);

        const previousScrollDistance =
            container.scrollHeight - container.scrollTop - container.clientHeight;
        const wasNearBottom = previousScrollDistance < 100;

        if (!messages.length) {
            container.innerHTML = `
                <div class="chat-date-label">YOUR CONVERSATION STARTS HERE</div>
                <div class="empty-state">No messages yet. Say hello!</div>`;
            return;
        }

        container.innerHTML = messages.map(message => {
            const mine = String(message.sender_id) === String(senderId);
            return `
                <div class="chat-message ${mine ? "mine" : "theirs"}">
                    <div class="message-text">${escapeHTML(message.message_text || message.content || "")}</div>
                    <span class="message-time">${escapeHTML(formatDate(message.created_at))}</span>
                </div>`;
        }).join("");

        if (!silent || wasNearBottom) {
            container.scrollTop = container.scrollHeight;
        }
    } catch (error) {
        if (!silent) {
            container.innerHTML =
                `<div class="empty-state">Could not load messages.<br>${escapeHTML(error.message)}</div>`;
        }
    }
}

async function sendMessage() {
    const senderId = getCurrentUserId();
    const recipientId = $("chatUser").value;
    const input = $("chatInput");
    const messageText = input.value.trim();

    if (!senderId) {
        showToast("Choose your user in the post creator first.");
        return;
    }
    if (!recipientId) {
        showToast("Choose a person to chat with.");
        return;
    }
    if (String(senderId) === String(recipientId)) {
        showToast("Choose a different person.");
        return;
    }
    if (!messageText) return;

    const sendButton = document.querySelector(".send-button");
    if (sendButton) sendButton.disabled = true;

    try {
        await apiJSON("/api/messages", jsonOptions("POST", {
            sender_id: Number(senderId),
            recipient_id: Number(recipientId),
            message_text: messageText
        }));

        input.value = "";
        await loadMessages();
    } catch (error) {
        showToast("Could not send message: " + error.message);
    } finally {
        if (sendButton) sendButton.disabled = false;
        input.focus();
    }
}

window.sendMessage = sendMessage;

$("chatInput").addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

/* Start application */

document.addEventListener("DOMContentLoaded", async () => {
    await loadUsers();
    await loadPosts();
});
