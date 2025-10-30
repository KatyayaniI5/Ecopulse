// Session Manager for handling multiple user sessions
class SessionManager {
  constructor() {
    this.SESSION_KEY = 'epics_session_id';
    this.USER_KEY = 'epics_user_id';
    this.init();
  }

  // Initialize session manager
  init() {
    // Generate a unique session ID if it doesn't exist
    if (!this.getSessionId()) {
      this.generateSessionId();
    }
  }

  // Generate a unique session ID
  generateSessionId() {
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem(this.SESSION_KEY, sessionId);
    return sessionId;
  }

  // Get current session ID
  getSessionId() {
    return localStorage.getItem(this.SESSION_KEY);
  }

  // Set user ID for current session
  setUserId(userId) {
    localStorage.setItem(this.USER_KEY, userId);
  }

  // Get user ID for current session
  getUserId() {
    return localStorage.getItem(this.USER_KEY);
  }

  // Check if current session matches stored user
  isSessionValid(userId) {
    const storedUserId = this.getUserId();
    return storedUserId === userId;
  }

  // Clear session data
  clearSession() {
    localStorage.removeItem(this.SESSION_KEY);
    localStorage.removeItem(this.USER_KEY);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
  }

  // Start new session for user
  startSession(userId) {
    // Clear any existing session
    this.clearSession();
    
    // Generate new session ID
    this.generateSessionId();
    
    // Set user ID
    this.setUserId(userId);
  }

  // Validate session before login
  validateSessionBeforeLogin(userId) {
    const currentUserId = this.getUserId();
    
    // If there's already a session with a different user, clear it
    if (currentUserId && currentUserId !== userId) {
      console.log('Different user session detected, clearing old session');
      this.clearSession();
      return false;
    }
    
    return true;
  }

  // Get session info for debugging
  getSessionInfo() {
    return {
      sessionId: this.getSessionId(),
      userId: this.getUserId(),
      hasTokens: !!(localStorage.getItem('access_token') && localStorage.getItem('refresh_token')),
      hasUserData: !!localStorage.getItem('user_data')
    };
  }
}

// Create singleton instance
const sessionManager = new SessionManager();

export default sessionManager; 