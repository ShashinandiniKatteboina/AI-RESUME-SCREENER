import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Register() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [role, setRole] = useState("candidate");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (event) => {

    event.preventDefault();

    setError("");
    setLoading(true);


    try {

      const response = await fetch(
        "http://127.0.0.1:5000/users",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            name: name,

            email: email,

            password: password,

            role: role

          })
        }
      );


      const data = await response.json();


      if (!response.ok) {

        setError(
          data.error || "Registration failed"
        );

        setLoading(false);

        return;
      }


      alert(
        "Account created successfully. Please login."
      );


      navigate("/login");

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
          Create Account
        </h1>

        <p className="auth-subtitle">
          Join the AI Resume Screener
        </p>


        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        <form onSubmit={handleSubmit}>

          <div className="form-group">

            <label>
              Full Name
            </label>

            <input
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(event) =>
                setName(event.target.value)
              }
              required
            />

          </div>


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
              placeholder="Create a password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />

          </div>


          <div className="form-group">

            <label>
              Account Type
            </label>


            <select
              value={role}
              onChange={(event) =>
                setRole(event.target.value)
              }
            >

              <option value="candidate">
                Candidate
              </option>

              <option value="recruiter">
                Recruiter
              </option>

            </select>

          </div>


          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >

            {loading
              ? "Creating account..."
              : "Create Account"
            }

          </button>

        </form>


        <p className="auth-footer">

          Already have an account?

          {" "}

          <Link to="/login">
            Login
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

export default Register;