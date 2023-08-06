#!/usr/bin/osascript

on run argv
  try
    set _APP_TIMEOUT to (item 1 of argv)
    with timeout of _APP_TIMEOUT seconds
      tell application "Brave Browser"
        repeat with w in  every window
          repeat with t in every tab in w
            set _tab_url to (URL of t as text)
          end repeat
        end repeat
      end tell
      return 1
    end timeout
  on error errorMessage number errorNumber
    --Connection is invalid. (-609)
    --AppleEvent timed out. (-1712)
    if (errorNumber is in {-609,-1712}) then return
    error errorMessage number errorNumber
  end try
end run
