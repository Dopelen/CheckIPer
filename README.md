# CheckIPer
Program for ping multiple devices and displaying results


## What does CheckIPer do?
* Receives a list of IP addresses required for verification with their description from a text file
* Checks them with the ping command
* Displays the result in a convenient form

`In additional!`

- Allows grouping of output
- Can ping automatically at specified time intervals
- Shows an error if the selected file does not match the formatting
- Allows you to select a file via the file manager and remembers your previous selection

***Just look at this cool demo***

https://github.com/Dopelen/CheckIPer/assets/141639888/99f040ee-ef7c-4b6a-811d-a176f6ea2a96

### Features in development
1. There is an asynchronous implementation that works much faster, but it is still unstable and not tied to the GUI
1. Also in operation is a screen for additional checking of servers that do not respond
1. Console implementation without GUI


### Input
Input is made from a text file selected after push button "Select file" or "Start"

Each IP address in txt file has its own line and description fields

Description fields go one after another in order:

**Address\tDescription\tPlace\tType**

Fields are separated by a single tab character ("**\t**")

><details>
><summary> Example: </summary>
>
>*google.com big searching service USA giga*
>
>*yandex.ru big searching service from Ru RU giga*
>
>in row format it would look like this:
>
>*google.com\tbig searching service\tUSA\tseporator\tgiga\n*
>
>*yandex.ru\tbig searching service from Ru\tRU\tgiga*
></details>

          
> [!WARNING]
><details>
><summary> Input quirks </summary>
> 
> * The file must not contain empty lines
> * The separator between fields is a single tab "\t"
> * If the field is expected to be empty, enter "-"
> * A common error (on all 4 computers that I checked :)) is a problem with the delimiter inside the text file, someeditors automatically convert tabs to spaces


#### Software which I used and also which you need to run it :

* ![4375050_logo_python_icon](https://github.com/Dopelen/CheckIPer/assets/141639888/dde41867-41d5-45cc-bd7d-dfbeb551fb47) ***Python 3.8***

* ![1266152](https://github.com/Dopelen/CheckIPer/assets/141639888/840aa4d1-150c-4317-aada-ab00ac637c3e) ***Kivy 2.3***

* File with font and icons with required images

**Everything should be stored in the folder with the launch file**


*small plus: The program itself checks the OS on which it is launched, so it should be workable on different systems*
