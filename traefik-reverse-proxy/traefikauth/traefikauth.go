package traefikauth

import (
	"context"
	"log"
	"net/http"
	"strings"
)

// Config holds plugin settings
type Config struct {
	AuthServiceURL string `json:"authServiceURL,omitempty"`
	BearerSecret   string `json:"bearerSecret,omitempty"`
}

// CreateConfig initializes default config
func CreateConfig() *Config {
	return &Config{}
}

// TraefikAuth middleware
type TraefikAuth struct {
	next         http.Handler
	authService  string
	bearerSecret string
	name         string
}

// New creates a new middleware instance
func New(ctx context.Context, next http.Handler, config *Config, name string) (http.Handler, error) {
	return &TraefikAuth{
		next:         next,
		authService:  config.AuthServiceURL,
		bearerSecret: config.BearerSecret,
		name:         name,
	}, nil
}
func (a *TraefikAuth) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
	path := req.URL.Path

	// Skip authentication for login and verify endpoints
	if path == "/login" || path == "/verify" {
		a.next.ServeHTTP(rw, req)
		return
	}

	log.Printf("traefikauth req handle: %v", path)
	log.Printf("traefikauth req handle")
	// 1. Check Bearer token for API clients
	authHeader := req.Header.Get("Authorization")
	if authHeader != "" && isValidBearer(authHeader, a.bearerSecret) {
		a.next.ServeHTTP(rw, req)
		log.Printf("authHeader found with valid bearer: %v", authHeader)
		return
	}

	log.Printf("no auth header")
	// 2. Check cookie for browser users
	sessionCookie, err := req.Cookie("session")
	if err == nil {
		log.Printf("found session cookie: Name=%s, Value=%s", sessionCookie.Name, sessionCookie.Value)
		if verifySession(sessionCookie.Value, a.authService) {
			a.next.ServeHTTP(rw, req)
			log.Printf("session verified: %v", sessionCookie.Value)
			log.Printf("url: %v", req.URL.RequestURI())
			return
		} else {
			log.Printf("session verification failed")
		}
	} else {
		log.Printf("no session cookie found: %v", err)
	}

	// 3. Determine if request is API or browser
	if isBrowser(req) {
		loginUrl := "https://www.959353d1958446d49b91832e0d8e21fa.online/login?next=" + req.URL.RequestURI()
		log.Printf("redirecting to loginUrl: %s", loginUrl)
		http.Redirect(rw, req, loginUrl, http.StatusSeeOther)
	} else {
		log.Printf("err Unauthorized")
		http.Error(rw, "Unauthorized", http.StatusUnauthorized)
	}
}

// Very simple browser detection
func isBrowser(req *http.Request) bool {
	ua := req.Header.Get("User-Agent")
	return ua != "" && !strings.HasPrefix(ua, "curl")
}

// Call auth-service to validate session cookie
func verifySession(cookieVal, authService string) bool {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", authService+"/verify", nil)
	req.AddCookie(&http.Cookie{Name: "session", Value: cookieVal})
	resp, err := client.Do(req)
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	return resp.StatusCode == 200
}

func isValidBearer(header string, secret string) bool {
	if !strings.HasPrefix(header, "Bearer ") {
		return false
	}
	return header[len("Bearer "):] == secret
}
