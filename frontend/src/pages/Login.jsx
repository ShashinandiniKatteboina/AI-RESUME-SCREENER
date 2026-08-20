import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (event) => {

    event.preventDefault();

    setError("");
    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:5000/login",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            email: email,
            password: password
          })
        }
      );


      const data = await response.json();


      if (!response.ok) {

        setError(
          data.error || "Login failed"
        );

        setLoading(false);

        return;
      }


      // Save JWT token
      localStorage.setItem(
        "token",
        data.token
      );


      // Save user information
      localStorage.setItem(
        "user",
        JSON.stringify(data.user)
      );


      // Go to dashboard
      navigate("/dashboard");

    }

    catch (error) {

      console.error(error);

      setError(
        "Unable to connect to the server."
      );

    }

    finally {

      setLoading(false);

    }
  };


  return (

    <div className="auth-page">

      <div className="auth-card">

        <h1>
          Welcome Back
        </h1>

        <p className="auth-subtitle">
          Login to your AI Resume Screener account
        </p>


        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        <form onSubmit={handleSubmit}>

          <div className="form-group">

            <label>
              Email
            </label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />

          </div>


          <div className="form-group">

            <label>
              Password
            </label>

            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />

          </div>


          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >

            {loading
              ? "Logging in..."
              : "Login"
            }

          </button>

        </form>


        <p className="auth-footer">

          Don't have an account?

          {" "}

          <Link to="/register">
            Create account
          </Link>

        </p>


        <Link
          to="/"
          className="back-home"
        >
          ← Back to Home
        </Link>

      </div>

    </div>

  );
}

export default Login;