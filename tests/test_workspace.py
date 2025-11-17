import re

from playwright.sync_api import expect

WORK_SPACE_NAME = "Test workspace"
TEST_EMAIL = "test@gmail.com"

def test_workspace_create(authenticated_context, base_url):
    """
    Test Case: Create a New Workspace

    Objective:
        Verify that a user can successfully create a new workspace.

    Precondition:
        The user must be logged in (authenticated session).

    Steps:
        1. Navigate to the 'Workspaces' page.
        2. Validate presence of the main 'Workspaces' heading.
        3. Ensure no existing 'Team Workspaces' section is visible initially.
        4. Open the workspace creation dialog.
        5. Fill in workspace name and description.
        6. Submit the creation form.
        7. Wait for the workspace list to refresh.
        8. Confirm the new workspace appears under 'Team Workspaces'.

    Expected Result:
        A newly created workspace should be displayed under 'Team Workspaces'.
    """
    page = authenticated_context.new_page()
    page.goto(f"{base_url}workspaces")

    # Verify navigation to the "Workspaces" page
    expect(page.get_by_role("heading", level=1, name="Workspaces")).to_be_visible()

    # Ensure there are no existing team workspaces
    expect(page.get_by_role("heading", name="Team Workspaces")).not_to_be_visible()

    # Open workspace creation modal
    page.get_by_role("button", name="Create Workspace").click()

    # Fill in workspace form fields
    page.get_by_role("textbox", name="Enter workspace name").fill(WORK_SPACE_NAME)
    page.get_by_role("textbox", name="Enter workspace description").fill("Testing workspace")

    # Submit the form to create the workspace
    page.get_by_role("button", name="Create", exact=True).click()

    # Wait briefly for UI updates / refresh
    page.wait_for_timeout(1000)

    # Validate that the new workspace appears under "Team Workspaces"
    expect(page.get_by_role("heading", name="Team Workspaces")).to_be_visible()
    expect(page.get_by_role("heading", name=WORK_SPACE_NAME)).to_be_visible()

    page.close()


def test_workspace_invite(authenticated_context, base_url):
    """
    Test Case: Invite a User to an Existing Workspace

    Objective:
        Verify that a user can successfully invite other members to a workspace.

    Precondition:
        A workspace must already exist (e.g., created by `test_workspace_create`).

    Steps:
        1. Navigate to the 'Workspaces' page.
        2. Validate that the workspace and team section are visible.
        3. Click the 'Invite Member' button.
        4. Enter one or more email addresses for invitation.
        5. Send the invitation.
        6. View sent invitations and verify presence of 'Resend' and 'Cancel' actions.
        7. Cancel an existing invitation and confirm visual feedback.

    Expected Result:
        Invitations should be listed under the workspace, with visible controls
        to resend or cancel invitations. After cancellation, an empty-state message appears.
    """
    page = authenticated_context.new_page()
    page.goto(f"{base_url}workspaces")

    # Validate main workspace section visibility
    expect(page.get_by_role("heading", level=1, name="Workspaces")).to_be_visible()
    expect(page.get_by_role("heading", name="Team Workspaces")).to_be_visible()
    expect(page.get_by_role("heading", name=WORK_SPACE_NAME)).to_be_visible()

    # Open the invitation dialog
    page.get_by_role("button", name="Invite Member").click()

    # Confirm that the invite modal is displayed
    expect(page.get_by_role("heading", name=f"Invite to {WORK_SPACE_NAME}")).to_be_visible()

    # Enter test email(s) and send invitation
    page.get_by_role("textbox", name="user1@example.com, user2@").fill(TEST_EMAIL)
    page.get_by_role("button", name="Send Invitation").click()

    # Wait for system response and UI update
    page.wait_for_timeout(1000)

    # View the list of sent invitations
    page.get_by_role("button", name="View Invitations").click()

    # Verify invitation management options
    expect(page.get_by_role("button", name="Resend All")).to_be_visible()
    expect(page.get_by_role("button", name="Resend Invitation")).to_be_visible()
    expect(page.get_by_role("heading", name=f"{WORK_SPACE_NAME} Invitations")).to_be_visible()

    # Cancel an existing invitation
    page.get_by_role("button", name="Cancel Invitation").click()

    # Ensure the no-pending-invitations message appears
    expect(page.get_by_text("No pending invitations for")).to_be_visible()

    # Verify the invitation modal can be dismissed safely
    page.locator("div").filter(
        has_text=re.compile(r"^Test workspace Invitations$")
    ).get_by_role("button").click()

    page.close()


def test_workspace_delete(authenticated_context, base_url):
    """
    Test Case: Delete an Existing Workspace

    Objective:
        Verify that a user can successfully delete a workspace.

    Precondition:
        At least one workspace (e.g., from `test_workspace_create`) must exist.

    Steps:
        1. Navigate to the 'Workspaces' page.
        2. Confirm the 'Team Workspaces' section and existing workspace visibility.
        3. Click the 'Delete Workspace' button.
        4. Handle the confirmation dialog by accepting it.
        5. Wait temporarily for any backend operations or UI updates.
        6. Verify that the deleted workspace and section are no longer displayed.

    Expected Result:
        The workspace should be removed from the UI and 'Team Workspaces'
        should no longer be visible.
    """
    page = authenticated_context.new_page()
    page.goto(f"{base_url}workspaces")

    # Auto-accept confirmation dialog when deleting a workspace
    page.on("dialog", lambda dialog: dialog.accept())

    # Confirm navigation and workspace existence
    expect(page.get_by_role("heading", level=1, name="Workspaces")).to_be_visible()
    expect(page.get_by_role("heading", name="Team Workspaces")).to_be_visible()
    expect(page.get_by_role("heading", name=WORK_SPACE_NAME)).to_be_visible()

    # Initiate workspace deletion
    page.get_by_role("button", name="Delete Workspace").click()

    # Wait for the deletion UI process to complete
    page.wait_for_timeout(1000)

    # Verify that the workspace and related section no longer appear
    expect(page.get_by_role("heading", name="Team Workspaces")).not_to_be_visible()
    expect(page.get_by_role("heading", name=WORK_SPACE_NAME)).not_to_be_visible()

    page.close()