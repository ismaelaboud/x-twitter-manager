# Twitter API Setup Guide

## Prerequisites
- Twitter Developer Account
- Python 3.8+
- Virtual Environment

## Steps to Set Up Twitter API Credentials

1. Create a Twitter Developer Account
   - Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - Sign in or create a new account
   - Apply for a Developer Account if needed

2. Create a New Project
   - In the Developer Portal, click "Projects & Apps"
   - Create a new Project
   - Create a new App within that project
   - Choose "User Authentication" as the primary use case

3. Generate Credentials
   - Navigate to "Keys and Tokens"
   - Generate:
     * Client ID
     * Client Secret
     * Bearer Token

4. Configure Callback URL
   - Set Callback URL to: `http://localhost:8000/auth/twitter`

5. Update .env File
   - Open `.env` in the backend directory
   - Replace placeholders with your actual credentials:
     ```
     TWITTER_CLIENT_ID=your_client_id
     TWITTER_CLIENT_SECRET=your_client_secret
     TWITTER_BEARER_TOKEN=your_bearer_token
     ```

6. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Scopes and Permissions
Current scopes:
- `tweet.read`: Read tweets
- `users.read`: Read user information
- `offline.access`: Refresh tokens

## Security Notes
- Never commit `.env` to version control
- Keep credentials confidential
- Rotate credentials periodically

## Troubleshooting
- Ensure all credentials are correct
- Check network connectivity
- Verify Twitter Developer Account status

## Support
For issues, contact Twitter Developer Support or create an issue in our GitHub repository.
