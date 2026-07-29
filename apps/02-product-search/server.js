const express = require("express");
const path = require("path");
const mysql = require("mysql2/promise");

const PORT = process.env.PORT || 3000;
const DB_HOST = process.env.DB_HOST || "db";
const DB_USER = process.env.DB_USER || "root";
const DB_PASSWORD = process.env.DB_PASSWORD || "rootpassword";
const DB_NAME = process.env.DB_NAME || "ctf02";

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

// VULNERABLE: the search term is concatenated directly into the LIKE
// pattern instead of being passed as a bound parameter. Errors are also
// returned verbatim to the client, which is its own real-world mistake
// (leftover debug behavior in production) that makes exploitation easier.
app.get("/search", async (req, res) => {
  const q = typeof req.query.q === "string" ? req.query.q : "";

  const query = `SELECT id, name, description, price FROM products WHERE name LIKE '%${q}%'`;

  try {
    const [rows] = await pool.query(query);
    return res.json({ results: rows });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

connectWithRetry().then(() => {
  app.listen(PORT, () => console.log(`[app] 02-product-search listening on ${PORT}`));
});
