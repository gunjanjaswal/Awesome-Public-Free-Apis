/**
 * This script ensures that the navigation links in the README.md file
 * always use the correct anchor format with emoji identifiers.
 * 
 * It's designed to be run as a pre-commit hook or as part of a GitHub Action.
 */

const fs = require('fs');
const path = require('path');

// Define the correct navigation bar with proper anchor links
const CORRECT_NAV_BAR = '[Browse APIs by Category](#card_index-api-categories---find-the-perfect-api-for-your-project) • [Trending GitHub Repositories](#rocket-trending-github-repositories) • [How to Contribute](#handshake-how-to-contribute-to-this-api-collection) • [Automation Details](#gear-how-our-automated-api-tracking-works) • [License](#page_with_curl-license) • [☕ Buy Me a Coffee](https://buymeacoffee.com/gunjanjaswal)';

// Path to the README.md file
const README_PATH = path.join(process.cwd(), 'README.md');

/**
 * Fix navigation links in README.md
 */
function fixNavigationLinks() {
  try {
    // Read the README.md file
    let readmeContent = fs.readFileSync(README_PATH, 'utf8');

    // Replace the navigation bar with the correct one
    const navPattern = /\[Browse APIs by Category\].*?\[License\]\([^)]+\)(?:\s•\s\[☕\sBuy\sMe\sa\sCoffee\]\(https:\/\/buymeacoffee\.com\/gunjanjaswal\))?/s;
    readmeContent = readmeContent.replace(navPattern, CORRECT_NAV_BAR);

    // Fix formatting issues with section headings
    readmeContent = readmeContent.replace(/(_Last updated: .*?)_##\s/g, '$1_\n\n## ');

    // Write the updated content back to the README.md file
    fs.writeFileSync(README_PATH, readmeContent, 'utf8');
    
    console.log('Navigation links fixed successfully.');
  } catch (error) {
    console.error(`Error fixing navigation links: ${error.message}`);
    process.exit(1);
  }
}

// Run the function
fixNavigationLinks();
