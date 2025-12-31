-- PMI Emergency Call System - Database Initialization
-- This file is automatically executed on first MySQL startup

-- Create database if not exists (already done by MYSQL_DATABASE env)
-- USE pmi_emergency;

-- Grant privileges
GRANT ALL PRIVILEGES ON pmi_emergency.* TO 'pmi_user'@'%';
FLUSH PRIVILEGES;
