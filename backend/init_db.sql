DROP DATABASE IF EXISTS poll_db;
CREATE DATABASE poll_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE poll_db;

CREATE TABLE poll (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question VARCHAR(255) CHARACTER SET utf8mb4 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE poll_option (
    id INT PRIMARY KEY AUTO_INCREMENT,
    poll_id INT NOT NULL,
    option_text VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL,
    vote_count INT DEFAULT 0,
    FOREIGN KEY (poll_id) REFERENCES poll(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 预置一份问卷和选项
INSERT INTO poll (id, question) VALUES (1, '你最喜欢哪种编程语言？');
INSERT INTO poll_option (poll_id, option_text) VALUES
    (1, 'Python'),
    (1, 'JavaScript'),
    (1, 'Java'),
    (1, 'C++'); 