-- Keep a log of any SQL queries you execute as you solve the mystery.

-- First checking the description

SELECT description FROM crime_scene_reports 
WHERE year = 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";

-- to check the transcripts and names from interviews
SELECT name, transcript FROM interviews
WHERE year = 2020 AND month = 7 AND day = 28;

-- checking car records
SELECT * FROM courthouse_security_logs;

-- tracking suspect from parking
SELECT name, hour, minute FROM people 
JOIN courthouse_security_logs ON courthouse_security_logs.license_plate = people.license_plate
WHERE  year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <=25 AND activity = "exit";
-- Patrick | 10 | 16
-- Ernest | 10 | 18
-- Amber | 10 | 18
-- Danielle | 10 | 19
-- Roger | 10 | 20
-- Elizabeth | 10 | 21
-- Russell | 10 | 23
-- Evelyn | 10 | 23

-- check atm records
SELECT account_number, amount FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";

-- collect person_id from bank acc
SELECT person_id, creation_year FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw");

--narrow down suspect from bank acc
SELECT name FROM people WHERE id IN 
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"));

-- current suspect
SELECT name FROM people WHERE license_plate IN 
(SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 16 AND minute <=25)
INTERSECT
SELECT name FROM people WHERE id IN 
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"));
-- Danielle
-- Elizabeth
-- Ernest
-- Russell

-- check earliest flight
SELECT * FROM flights WHERE year = 2020 AND month = 7 AND day = 29;
-- origin = 8, destination = 4, flight id = 36;

-- track passport;
SELECT passport_number FROM passengers WHERE flight_id = 36;

-- suspect from flight
SELECT name FROM people where passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

-- the suspects
SELECT name FROM people WHERE license_plate IN 
(SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 16 AND minute <=25)
INTERSECT
SELECT name FROM people WHERE id IN 
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"))
INTERSECT
SELECT name FROM people where passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);
--Danielle
--Ernest

-- the city where the theif escaped
SELECT * FROM airports WHERE id = 4;
--LONDON

-- phone record
SELECT name FROM people WHERE phone_number IN (SELECT  caller FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60);
-- thief is Ernest!
--accomplice
SELECT name FROM people WHERE phone_number = (SELECT phone_calls.receiver FROM people 
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE name = "Ernest" AND year = 2020 AND month = 7 AND day = 28 AND duration < 60);