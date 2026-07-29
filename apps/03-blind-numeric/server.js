const express = require("express");
const path = require("path");
const mysql = require("mysql2/promise");

const PORT = process.env.PORT || 3000;
const DB_HOST = process.env.DB_HOST || "db";
const DB_USER = process.env.DB_USER || "root";
const DB_PASSWORD = process.env.DB_PASSWORD || "rootpassword";
const DB_NAME = process.env.DB_NAME || "ctf03";

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
app.use(express.static(path.join(__dirname, "public")));

// VULNERABLE: `id` is assumed to always be numeric, so it is never quoted
// or validated (no parseInt/Number check) before being concatenated into
// the query. The response never echoes data - only whether a row matched -
// which is why this has to be exploited blind.
app.get("/api/user", async (req, res) => {
  const id = req.query.id;
  if (id === undefined) {
    return res.status(400).json({ error: "id is required" });
  }

  const query = `SELECT username FROM users WHERE id = ${id}`;

  try {
    const [rows] = await pool.query(query);
    return res.json({ found: rows.length > 0 });
  } catch (err) {
    // Only a generic failure is reported - no query details leak here,
    // unlike 02. This challenge is intentionally truly blind.
    return res.status(400).json({ found: false });
  }
});

connectWithRetry().then(() => {
  app.listen(PORT, () => console.log(`[app] 03-blind-numeric listening on ${PORT}`));
});
