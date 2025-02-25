export function getSessionId(): string {
    let sessionId = localStorage.getItem("sessionId");
    if (!sessionId) {
        sessionId = `user_${Math.random().toString(36).slice(2, 11)}`; 
        localStorage.setItem("sessionId", sessionId);
    }
    return sessionId;
}
