# Secrets #

This small program generates a random password. The user can specify password length, minimum quantity of Upercase letters, lowecase letters, digits and special characters. Some site won't accept all special character but some, the app accept an sample of special character to choose from.

## Motivation for creating this app ##

I was looking for a reason to learn about the [Secret library](https://docs.python.org/3/library/secrets.html) and I don't trusth password generator out there (call me old fashion ;-) )

## How to run this app ##

there are two ways to run it, both ways will use the default configuration, meaning 20 character
long and making sure at least one upper case character, one lower case characer, one digit and one
special character are being used.

1. pipenv:
    make sure you have python 3.10.0 and pipenv install on your machine and then:

    ```sh
    pipenv shell
    ./run.py
    ```

2. docker:

    ```sh
    docker build --rm -t secrets:latest .
    docker run --rm -t --name secrets-container secrets:latest
    ```

## How to run this app with custom parameters ##

```sh
# Using pipenv

./run.py -h # to get help
./run.py ./run.py -l 30 -p *+-:;<=>?

# Using docker
docker run --rm --name secrets-container -t -e LENGTH=30 -e MIN_PATTER=2 -e  SPECIAL_CHAR="*+-:;<=>?" secrets:latest
```

## Future plans ##

<!-- REFERENCE: https://mermaid-js.github.io/mermaid/#/ -->
The idea is to make a webapp hosted in AWS that allows multiple users. We would use OAuth2 with google/twitter/github
for authentication.

once the user is logged in it will see a search field. They will use this search field to find the credentials they are looking for. They can use either *name* or *url*. Then the app will show some imformation and other will be redacted,
however, they click on copy button (to copy the information to memory). No sensitive information (user/password) will be shown at any point.

```mermaid
flowchart TB
    start([User visit page/load app])
    login{Is user logged in?}
    login_display[Display logging screen]
    login_process[Redirect user to OAuth provider]
    display_main_screen[Display main screen]
    what_to_do{What does the user want to do?}
    user_search[/User search for cred using name or url/]
    cred_found{Is credentials found?}
    display_cred[Display credential]
    cred_not_found[Display error message]
    cred_not_valid[Display error message]
    display_password_form[Display new credential form]
    display_search_form[Display search credential form]
    display_password_again1{Is new credential valid?}
    display_password_again2{does credential alreary exist?}
    user_add_cred[/User add new credentials/]
    actions{now what?}
    copy[Either password or user is copied to memory]
    delete[Credentials are deleted]
    update[Credentials are updated]
    save[New credential is saved]
    want_close{Does the user want to continue?}

    start-->login
    login -->|Yes| display_main_screen
    login -->|No| login_display
    login_display --> login_process
    login_process --> display_main_screen
    display_main_screen --> what_to_do
    what_to_do -->|Search| display_search_form
    what_to_do -->|Add| display_password_form
    display_password_form --> user_add_cred
    display_search_form --> user_search
    user_add_cred -->display_password_again1
    display_password_again1 -->|Yes| display_password_again2
    display_password_again1 -->|No| cred_not_valid
    display_password_again2 -->|Yes| save
    display_password_again2 -->|No| cred_not_valid
    cred_not_valid --> user_add_cred
    user_search --> cred_found
    cred_found -->|Yes| display_cred
    cred_found -->|No| cred_not_found
    cred_not_found --> display_search_form
    display_cred --> actions
    actions --> copy
    actions --> delete
    actions --> update
    delete --> display_main_screen
    update --> display_main_screen
    copy --> want_close
    want_close -->|yes| actions
    want_close -->|No| display_main_screen
```

<!-- https://sparxsystems.com/resources/tutorials/uml/datamodel.html -->

```mermaid
erDiagram
    SESSION }o--|| ACCOUNT-SESSION : belong
    SESSION {
        string id PK
        string account FK
        string token1
        string token2
        date expired
    }
    ACCOUNT ||--o{ ACCOUNT-PASSWORD : has
    ACCOUNT ||--o{ ACCOUNT-SESSION : in
    ACCOUNT {
        string id PK
        string name
        string email
        string provider
    }
    PASSWORD }o--|| ACCOUNT-PASSWORD : belong
    PASSWORD {
        string id PK
        date utc_date
        string name
        string url
        string account FK
        byte password
    }
```
