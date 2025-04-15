-- Clear existing data to avoid duplicate entries
DELETE FROM Users;
DELETE FROM Students;
DELETE FROM Tutors;
DELETE FROM Admins;
DELETE FROM Payments;

-- Insert data into Users table first
INSERT OR IGNORE INTO Users (user_id, role, email, password, name, profile_picture, MFA_enabled) VALUES
(1, 'student', 'student1@example.com', 'hashed_password1', 'Student One', NULL, 1),
(2, 'tutor', 'tutor1@example.com', 'hashed_password2', 'Tutor One', NULL, 0),
(3, 'admin', 'admin1@example.com', 'hashed_password3', 'Admin One', NULL, 1);

-- Insert data into Students table first
INSERT OR IGNORE INTO Students (student_id, payment_method) VALUES
(1, NULL);

-- Insert data into Tutors table first
INSERT OR IGNORE INTO Tutors (tutor_id, bio, hourly_rate, calendar_sync_enabled) VALUES
(2, 'Experienced Math Tutor', 25.50, 1);

-- Now insert into Payments table after Students and Tutors exist
INSERT OR IGNORE INTO Payments (payment_id, student_id, tutor_id, amount, payment_method, status) VALUES
(1, 1, 2, 25.50, 'Credit Card', 'Completed');

-- Insert data into Admins table
INSERT OR IGNORE INTO Admins (admin_id) VALUES
(3);

-- Insert data into Subjects table
INSERT OR IGNORE INTO Subjects (subject_id, subject_name) VALUES
(1, 'Mathematics'),
(2, 'Physics');

-- Insert data into StudentSubjects table
INSERT OR IGNORE INTO StudentSubjects (student_id, subject_id) VALUES
(1, 1);

-- Insert data into Certifications table
INSERT OR IGNORE INTO Certifications (cert_id, tutor_id, certification_name, issued_by, issued_date, expiry_date) VALUES
(1, 2, 'Math Teaching Certificate', 'Education Board', '2023-01-01', '2026-01-01');

-- Insert data into Expertise table
INSERT OR IGNORE INTO Expertise (expertise_id, expertise_name) VALUES
(1, 'Algebra'),
(2, 'Calculus');

-- Insert data into TutorExpertise table
INSERT OR IGNORE INTO TutorExpertise (tutor_id, expertise_id) VALUES
(2, 1);

-- Insert data into Privileges table
INSERT OR IGNORE INTO Privileges (privilege_id, privilege_name) VALUES
(1, 'Manage Users'),
(2, 'Manage Payments');

-- Insert data into AdminPrivileges table
INSERT OR IGNORE INTO AdminPrivileges (admin_id, privilege_id) VALUES
(3, 1);

-- Insert data into Sessions table
INSERT OR IGNORE INTO Sessions (session_id, student_id, tutor_id, status, session_date, duration, meeting_type) VALUES
(1, 1, 2, 'scheduled', '2025-03-01 10:00:00', 60, 'online');

-- Insert data into Reviews table
INSERT OR IGNORE INTO Reviews (review_id, student_id, tutor_id, rating, feedback_text) VALUES
(1, 1, 2, 5, 'Great tutor, very helpful!');

-- Insert data into Earnings table
INSERT OR IGNORE INTO Earnings (earning_id, tutor_id, total_income, pending_balance) VALUES
(1, 2, 25.50, 0.00);

-- Insert data into Chats table
INSERT OR IGNORE INTO Chats (message_id, sender_id, receiver_id, message_text, timestamp) VALUES
(1, 1, 2, 'Hello, I need help with algebra.', '2025-02-20 14:00:00');

-- Insert data into Files table
INSERT OR IGNORE INTO Files (file_id, uploader_id, file_url, session_id) VALUES
(1, 1, 'https://example.com/file1.pdf', 1);

-- Insert data into Disputes table
INSERT OR IGNORE INTO Disputes (dispute_id, student_id, tutor_id, issue_description, status) VALUES
(1, 1, 2, 'Session was not conducted properly', 'Pending');

-- Insert data into Announcements table
INSERT OR IGNORE INTO Announcements (announcement_id, admin_id, title, message_body, timestamp) VALUES
(1, 3, 'Platform Maintenance', 'The system will be down for maintenance.', '2025-02-25 12:00:00');

-- Insert data into SiteHealth table
INSERT OR IGNORE INTO SiteHealth (log_id, error_type, server_status, response_time) VALUES
(1, 'Timeout Error', 'Operational', 200.5);
