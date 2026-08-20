import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";


function Home() {

  return (

    <div className="app">

      <section className="hero">

        <nav className="navbar">

          <div className="logo">
            AI Resume Screener
          </div>

          <div className="nav-links">

            <a href="/login">
              Login
            </a>

            <a
              href="/register"
              className="nav-button"
            >
              Get Started
            </a>

          </div>

        </nav>


        <div className="hero-content">

          <div className="hero-text">

            <h1>
              Smart Resume Screening
              <br />
              Powered by AI
            </h1>

            <p>
              Analyze your resume, compare it with
              job requirements, identify skill gaps,
              and get AI-powered recommendations.
            </p>


            <div className="hero-buttons">

              <a
                href="/register"
                className="primary-button"
              >
                Get Started
              </a>


              <a
                href="/login"
                className="secondary-button"
              >
                Login
              </a>

            </div>

          </div>

        </div>

      </section>


      <section className="features">

        <div className="section-header">

          <h2>
            Everything You Need
          </h2>

          <p>
            A complete platform for candidates and recruiters.
          </p>

        </div>


        <div className="feature-grid">

          <div className="feature-card">

            <div className="feature-icon">
              📄
            </div>

            <h3>
              Resume Analysis
            </h3>

            <p>
              Upload your resume and automatically
              extract important information.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-icon">
              🎯
            </div>

            <h3>
              Match Score
            </h3>

            <p>
              Compare your skills with job requirements
              and calculate your compatibility score.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-icon">
              🤖
            </div>

            <h3>
              AI Analysis
            </h3>

            <p>
              Get AI-powered strengths, skill gaps
              and personalized recommendations.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-icon">
              🏢
            </div>

            <h3>
              Recruiter Screening
            </h3>

            <p>
              Recruiters can create jobs and
              screen candidates.
            </p>

          </div>

        </div>

      </section>


      <section className="cta">

        <h2>
          Ready to Analyze Your Resume?
        </h2>

        <p>
          Start your AI-powered resume analysis today.
        </p>


        <a
          href="/register"
          className="primary-button"
        >
          Create Account
        </a>

      </section>


      <footer>

        <p>
          © 2026 AI Resume Screener
        </p>

      </footer>

    </div>

  );
}


function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

      </Routes>

    </BrowserRouter>

  );
}


export default App;