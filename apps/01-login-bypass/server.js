const express = require("express");
const path = require("path");
const mysql = require("mysql2/promise");

const PORT = process.env.PORT || 3000;
const DB_HOST = process.env.DB_HOST || "db";
const DB_USER = process.env.DB_USER || "root";
const DB_PASSWORD = process.env.DB_PASSWORD || "rootpassword";
const DB_NAME = process.env.DB_NAME || "ctf01";

const FLAG = process.env.FLAG || "FLAG{login_bypass_plaintext_and_string_concat}";

let pool;

async function connectWithRetry(retries = 20, delayMs = 2000) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      pool = mysql.createPool({
        host: DB_HOST,
        user: DB_USER,
        password: DB_PASSWORD,
        database: DB_NAME,
        waitForConnections: true,
        connectionLimit: 10,
      });
      await pool.query("SELECT 1");
      console.log("[db] connected");
      return;
    } catch (err) {
      console.log(`[db] not ready (attempt ${attempt}/${retries}): ${err.message}`);
      await new Promise((r) => setTimeout(r, delayMs));
    }
  }
  throw new Error("could not connect to database");
}

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// VULNERABLE: username and password are concatenated directly into the SQL
// string instead of using a parameterized query. This is the classic
// "we'll just build the WHERE clause from user input" mistake.
app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  if (typeof username !== "string" || typeof password !== "string") {
    return res.status(400).send("username and password are required");
  }

  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

  try {
    const [rows] = await pool.query(query);
    if (rows.length === 0) {
      return res.status(401).send("Login failed. <a href='/'>back</a>");
    }
    const user = rows[0];
    if (user.is_admin) {
      return res.send(`
        <h1>Admin dashboard</h1>
        <p>Welcome, ${user.username}.</p>
        <p>${FLAG}</p>
      `);
    }
    return res.send(`<h1>Welcome, ${user.username}</h1><p>You are not an admin.</p>`);
  } catch (err) {
    return res.status(500).send(`SQL error: ${err.message}`);
  }
});

connectWithRetry().then(() => {
  app.listen(PORT, () => console.log(`[app] 01-login-bypass listening on ${PORT}`));
});
