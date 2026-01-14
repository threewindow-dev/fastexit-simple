-- Users table initialization
-- Dependencies: None
-- Description: Core user management table

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insert sample data (for development only)
-- This section should be removed or conditional in production
INSERT INTO users (username, email, full_name)
SELECT 'john_doe', 'john@example.com', 'John Doe'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'john_doe');

INSERT INTO users (username, email, full_name)
SELECT 'jane_smith', 'jane@example.com', 'Jane Smith'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'jane_smith');

INSERT INTO users (username, email, full_name)
SELECT 'bob_wilson', 'bob@example.com', 'Bob Wilson'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'bob_wilson');
