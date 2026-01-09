import { useState } from "react";
import { login, register } from "../api/testApi";

interface AuthPageProps {
  onAuth: () => void;
}

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "1rem",
  },
  card: {
    background: "var(--bg-secondary)",
    border: "1px solid var(--border-color)",
    borderRadius: "16px",
    padding: "2rem",
    width: "100%",
    maxWidth: "380px",
  },
  header: {
    textAlign: "center" as const,
    marginBottom: "1.5rem",
  },
  logo: {
    width: "48px",
    height: "48px",
    background: "linear-gradient(135deg, var(--accent) 0%, #f59e0b 100%)",
    borderRadius: "12px",
    margin: "0 auto 1rem",
  },
  title: {
    fontSize: "1.5rem",
    fontWeight: 600,
    color: "var(--text-primary)",
    margin: "0 0 0.25rem 0",
  },
  subtitle: {
    fontSize: "0.9rem",
    color: "var(--text-muted)",
    margin: 0,
  },
  form: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "1rem",
  },
  inputGroup: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "0.35rem",
  },
  label: {
    fontSize: "0.85rem",
    fontWeight: 500,
    color: "var(--text-secondary)",
  },
  input: {
    width: "100%",
    padding: "0.65rem 0.85rem",
    fontSize: "0.95rem",
  },
  submitBtn: {
    width: "100%",
    padding: "0.75rem",
    marginTop: "0.5rem",
    fontSize: "0.95rem",
    fontWeight: 600,
  },
  switchText: {
    textAlign: "center" as const,
    marginTop: "1.25rem",
    fontSize: "0.9rem",
    color: "var(--text-secondary)",
  },
  switchLink: {
    color: "var(--accent)",
    cursor: "pointer",
    fontWeight: 500,
  },
  error: {
    background: "#fef2f2",
    border: "1px solid #fecaca",
    borderRadius: "8px",
    padding: "0.75rem",
    color: "#991b1b",
    fontSize: "0.85rem",
    textAlign: "center" as const,
  },
  success: {
    background: "#ecfdf5",
    border: "1px solid #a7f3d0",
    borderRadius: "8px",
    padding: "0.75rem",
    color: "#065f46",
    fontSize: "0.85rem",
    textAlign: "center" as const,
  },
};

export default function AuthPage({ onAuth }: AuthPageProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!email || !password) {
      setError("Please fill in all fields");
      return;
    }

    if (mode === "register" && password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      if (mode === "register") {
        await register(email, password);
        setSuccess("Account created! You can now log in.");
        setMode("login");
        setPassword("");
        setConfirmPassword("");
      } else {
        await login(email, password);
        onAuth();
      }
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <div style={styles.logo} />
          <h1 style={styles.title}>Asset Tracker</h1>
          <p style={styles.subtitle}>
            {mode === "login" ? "Sign in to your account" : "Create a new account"}
          </p>
        </div>

        <form style={styles.form} onSubmit={handleSubmit}>
          {error && <div style={styles.error}>{error}</div>}
          {success && <div style={styles.success}>{success}</div>}

          <div style={styles.inputGroup}>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={styles.input}
              autoComplete="email"
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              autoComplete={mode === "login" ? "current-password" : "new-password"}
            />
          </div>

          {mode === "register" && (
            <div style={styles.inputGroup}>
              <label style={styles.label}>Confirm Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                style={styles.input}
                autoComplete="new-password"
              />
            </div>
          )}

          <button
            type="submit"
            className="primary"
            style={styles.submitBtn}
            disabled={loading}
          >
            {loading ? "Please wait..." : mode === "login" ? "Sign In" : "Create Account"}
          </button>
        </form>

        <p style={styles.switchText}>
          {mode === "login" ? (
            <>
              Don't have an account?{" "}
              <span style={styles.switchLink} onClick={() => { setMode("register"); setError(""); setSuccess(""); }}>
                Sign up
              </span>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <span style={styles.switchLink} onClick={() => { setMode("login"); setError(""); setSuccess(""); }}>
                Sign in
              </span>
            </>
          )}
        </p>
      </div>
    </div>
  );
}
