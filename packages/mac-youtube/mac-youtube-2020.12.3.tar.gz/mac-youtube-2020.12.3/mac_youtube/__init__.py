__all__ = ['pause', 'play', 'playing_urls', 'isplaying', 'urls', 'id', 'info']


import applescript
import google_chrome
import youtube_dl


def pause():
    """pause youtube videos"""
    code = """
on function()
    tell application "Google Chrome"
        repeat with w in every window
            repeat with t in every tab of w
                if "youtube" is in (get URL of t) then
                    tell t
                        set is_playing to execute javascript "!!Array.prototype.find.call(document.querySelectorAll('audio,video'),function(elem){return elem.duration > 0 && !elem.paused})"
                        if is_playing is true then
                            execute javascript "document.getElementsByClassName('ytp-play-button ytp-button')[0].click();"
                        end if
                    end tell
                end if
            end repeat
        end repeat
    end tell
end function

try
    function()
on error errorMessage number errorNumber
    if errorNumber is equal to -1719 then
        return
    end if
    error errorMessage number errorNumber
end try
"""
    return applescript.run(code)


def play():
    """continue play youtube video"""
    code = """
on function()
    tell application "Google Chrome"
        repeat with w in every window
            repeat with t in every tab of w
                if "youtube" is in (get URL of t) then
                    tell t
                        set is_playing to execute javascript "!!Array.prototype.find.call(document.querySelectorAll('audio,video'),function(elem){return elem.duration > 0 && !elem.paused})"
                        if is_playing is true then
                            return
                        end if
                    end tell
                end if
            end repeat
        end repeat

        repeat with w in every window
            repeat with t in every tab of w
                if "youtube" is in (get URL of t) then
                    tell t
                        set is_playing to execute javascript "!!Array.prototype.find.call(document.querySelectorAll('audio,video'),function(elem){return elem.duration > 0 && !elem.paused})"
                        if is_playing is false then
                            execute javascript "document.getElementsByClassName('ytp-play-button ytp-button')[0].click();"
                            return
                        end if
                    end tell
                end if
            end repeat
        end repeat
    end tell
end function

try
    function()
on error errorMessage number errorNumber
    if errorNumber is equal to -1719 then
        return
    end if
    error errorMessage number errorNumber
end try
"""
    return applescript.run(code)


def playing_urls():
    """return a list of playing urls"""
    code = """
on function()
    tell application "Google Chrome"
        repeat with w in every window
            repeat with t in every tab of w
                if "youtube" is in (get URL of t) then
                    tell t
                        set is_playing to execute javascript "!!Array.prototype.find.call(document.querySelectorAll('audio,video'),function(elem){return elem.duration > 0 && !elem.paused})"
                        if is_playing is true then
                            log (get URL of t)
                        end if
                    end tell
                end if
            end repeat
        end repeat
    end tell
end function

try
    function()
on error errorMessage number errorNumber
    if errorNumber is equal to -1719 then
        return
    end if
    error errorMessage number errorNumber
end try
    """
    return applescript.run(code).err.splitlines()


def isplaying():
    """return True if youtube video is playing"""
    return len(playing_urls()) > 0


def urls():
    """return a list of opened youtube videos"""
    return list(filter(lambda url: "www.youtube.com/" in url, google_chrome.urls()))


def id(url):
    """return video id"""
    return url.split("/")[-1] if "=" not in url else url.split("=")[1]


def info(video):
    """return info dictionary"""
    url = 'https://www.youtube.com/watch?v=%s' % id(video)
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        return ydl.extract_info(url, download=False)
