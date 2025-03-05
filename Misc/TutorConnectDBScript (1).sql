CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    role TEXT,
    email TEXT UNIQUE,
    password TEXT,
    name TEXT,
    profile_picture TEXT,
    MFA_enabled BOOLEAN
);

CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY,
    payment_method INTEGER,
    FOREIGN KEY (student_id) REFERENCES Users(user_id),
    FOREIGN KEY (payment_method) REFERENCES Payments(payment_id)
);

CREATE TABLE Tutors (
    tutor_id INTEGER PRIMARY KEY,
    bio TEXT,
    hourly_rate DECIMAL,
    calendar_sync_enabled BOOLEAN,
    FOREIGN KEY (tutor_id) REFERENCES Users(user_id)
);

CREATE TABLE SavedTutors (
    student_id INTEGER,
    tutor_id INTEGER,
    PRIMARY KEY (student_id, tutor_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id)
);

CREATE TABLE Subjects (
    subject_id INTEGER PRIMARY KEY,
    subject_name TEXT
);

CREATE TABLE StudentSubjects (
    student_id INTEGER,
    subject_id INTEGER,
    PRIMARY KEY (student_id, subject_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

CREATE TABLE Certifications (
    cert_id INTEGER PRIMARY KEY,
    tutor_id INTEGER,
    certification_name TEXT,
    issued_by TEXT,
    issued_date DATE,
    expiry_date DATE,
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id)
);

CREATE TABLE Expertise (
    expertise_id INTEGER PRIMARY KEY,
    expertise_name TEXT
);

CREATE TABLE TutorExpertise (
    tutor_id INTEGER,
    expertise_id INTEGER,
    PRIMARY KEY (tutor_id, expertise_id),
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id),
    FOREIGN KEY (expertise_id) REFERENCES Expertise(expertise_id)
);

CREATE TABLE Admins (
    admin_id INTEGER PRIMARY KEY,
    FOREIGN KEY (admin_id) REFERENCES Users(user_id)
);

CREATE TABLE Privileges (
    privilege_id INTEGER PRIMARY KEY,
    privilege_name TEXT
);

CREATE TABLE AdminPrivileges (
    admin_id INTEGER,
    privilege_id INTEGER,
    PRIMARY KEY (admin_id, privilege_id),
    FOREIGN KEY (admin_id) REFERENCES Admins(admin_id),
    FOREIGN KEY (privilege_id) REFERENCES Privileges(privilege_id)
);

CREATE TABLE Sessions (
    session_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    tutor_id INTEGER,
    status TEXT,
    session_date DATETIME,
    duration INTEGER,
    meeting_type TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id)
);

CREATE TABLE Reviews (
    review_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    tutor_id INTEGER,
    rating INTEGER,
    feedback_text TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id)
);

CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    tutor_id INTEGER,
    amount DECIMAL,
    payment_method TEXT,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id)
);

CREATE TABLE Earnings (
    earning_id INTEGER PRIMARY KEY,
    tutor_id INTEGER,
    total_income DECIMAL,
    pending_balance DECIMAL,
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id)
);

CREATE TABLE Chats (
    message_id INTEGER PRIMARY KEY,
    sender_id INTEGER,
    receiver_id INTEGER,
    message_text TEXT,
    timestamp DATETIME,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
);

CREATE TABLE Files (
    file_id INTEGER PRIMARY KEY,
    uploader_id INTEGER,
    file_url TEXT,
    session_id INTEGER,
    FOREIGN KEY (uploader_id) REFERENCES Users(user_id),
    FOREIGN KEY (session_id) REFERENCES Sessions(session_id)
);

CREATE TABLE Disputes (
    dispute_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    tutor_id INTEGER,
    issue_description TEXT,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (tutor_id) REFERENCES Tutors(tutor_id)
);

CREATE TABLE Announcements (
    announcement_id INTEGER PRIMARY KEY,
    admin_id INTEGER,
    title TEXT,
    message_body TEXT,
    timestamp DATETIME,
    FOREIGN KEY (admin_id) REFERENCES Admins(admin_id)
);

CREATE TABLE SiteHealth (
    log_id INTEGER PRIMARY KEY,
    error_type TEXT,
    server_status TEXT,
    response_time DECIMAL
);
