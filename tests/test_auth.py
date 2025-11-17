import re

import pytest
from playwright.sync_api import expect


def test_login_success(authenticated_context, base_url):
    """
    Verify that an authenticated user can successfully access the upload page.

    Steps:
        1. Open a new page using an authenticated browser context.
        2. Navigate to the upload page.
        3. Assert that the 'Chat' heading is visible, confirming successful login.
    """
    page = authenticated_context.new_page()
    page.goto(f"{base_url}upload")

    # Assert that the user is logged in and on the correct page
    expect(page.get_by_role("heading", name="Chat")).to_be_visible()

    page.close()


def test_remember_me(authenticated_context, base_url):
    """
    Verify that the 'Remember me' functionality behaves as expected
    (currently expected to fail due to an unimplemented feature).

    Steps:
        1. Open a new page using an authenticated browser context.
        2. Navigate to the settings page.
        3. Verify the 'Settings' heading is visible.
        4. Click on the 'Security' tab.
        5. Confirm 'Security Settings' text is visible.
        6. Wait shortly for UI updates.
        7. Verify that 'No trusted devices' heading is not visible (expected to fail).
    """
    page = authenticated_context.new_page()
    page.goto(f"{base_url}settings")

    # Confirm navigation to the Settings page
    expect(page.get_by_role("heading", name="Settings")).to_be_visible()

    # Navigate to the Security section
    page.get_by_role("button", name="Security").click()
    expect(page.get_by_text("Security Settings")).to_be_visible()

    # Small delay to stabilize test execution
    page.wait_for_timeout(1000)

    # This is an expected failure placeholder until feature is functional
    expect(page.get_by_role("heading", name="No trusted devices")).not_to_be_visible()

    page.close()


@pytest.mark.order("last")
def test_logout_success(authenticated_context, base_url):
    """
    Verify that a logged-in user can successfully log out.

    Steps:
        1. Navigate to the upload page using an authenticated context.
        2. Open the user menu and click 'Sign out'.
        3. Confirm the user is redirected to the login page.
        4. Verify that the login form is visible again.
    """
    page = authenticated_context.new_page()
    page.goto(f"{base_url}upload")

    # Perform logout
    page.get_by_role("button", name="GM").click()
    page.get_by_role("button", name="Sign out").click()

    # Assert redirection to login page
    expect(page).to_have_url(f"{base_url}login")

    # Confirm login form is visible
    expect(page.get_by_role("button", name=re.compile("sign in", re.I))).to_be_visible()

    page.close()


def test_logout_incorrect_password(browser_context, base_url, email, password):
    """
    Verify that login fails when provided with an incorrect password.

    Steps:
        1. Open a new browser page.
        2. Navigate to the login page.
        3. Fill in the login form using incorrect credentials.
        4. Submit the form.
        5. Verify that the 'Login failed' message appears.
    """
    page = browser_context.new_page()
    page.goto(f"{base_url}login")

    # Fill in login credentials
    page.get_by_role("textbox", name="Username, Email or Phone").fill(email)
    page.get_by_placeholder("Email").fill("some_email@gmail.com")
    page.get_by_placeholder("Password").fill(password)

    # Click the 'Remember me' checkbox
    page.locator("div").filter(has_text=re.compile(r"^Remember me$")).click()

    # Submit the login form
    page.get_by_role("button", name="Sign in").click()

    # Validate that a login failure message appears
    expect(page.get_by_text("Login failed. Please check")).to_be_visible()

    page.close()
