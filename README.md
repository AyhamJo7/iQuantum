# Ultimate Collection of Awesome Lists

A beautiful, searchable web interface that showcases curated resources from multiple GitHub awesome lists in one place. The data is automatically updated daily using GitHub Actions.

![Ultimate Collection Screenshot](screenshot.png)

## ✨ Features

- **Beautiful UI**: Dark-themed interface with star animation and aurora effects
- **Advanced Search**: Search across all resources, categories, and lists
- **Filtered Content**: All resources are validated to have working URLs
- **Automatic Updates**: Daily updates from source repositories via GitHub Actions
- **Responsive Design**: Works great on mobile and desktop devices

## 📚 Awesome Lists Included

- [vinta/awesome-python](https://github.com/vinta/awesome-python)
- [awesome-selfhosted/awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)
- [avelino/awesome-go](https://github.com/avelino/awesome-go)
- [Hack-with-Github/Awesome-Hacking](https://github.com/Hack-with-Github/Awesome-Hacking)
- [jaywcjlove/awesome-mac](https://github.com/jaywcjlove/awesome-mac)
- [MunGell/awesome-for-beginners](https://github.com/MunGell/awesome-for-beginners)
- [enaqx/awesome-react](https://github.com/enaqx/awesome-react)
- [fffaraz/awesome-cpp](https://github.com/fffaraz/awesome-cpp)
- [binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability)
- [sindresorhus/awesome-nodejs](https://github.com/sindresorhus/awesome-nodejs)
- [Solido/awesome-flutter](https://github.com/Solido/awesome-flutter)
- [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust)
- [vsouza/awesome-ios](https://github.com/vsouza/awesome-ios)
- [dkhamsing/open-source-ios-apps](https://github.com/dkhamsing/open-source-ios-apps)
- [brillout/awesome-react-components](https://github.com/brillout/awesome-react-components)
- [serhii-londar/open-source-mac-os-apps](https://github.com/serhii-londar/open-source-mac-os-apps)
- [akullpp/awesome-java](https://github.com/akullpp/awesome-java)
- [docker/awesome-compose](https://github.com/docker/awesome-compose)
- [alebcay/awesome-shell](https://github.com/alebcay/awesome-shell)
- [veggiemonk/awesome-docker](https://github.com/veggiemonk/awesome-docker)
- [ziadoz/awesome-php](https://github.com/ziadoz/awesome-php)
- [viatsko/awesome-vscode](https://github.com/viatsko/awesome-vscode)
- [matteocrippa/awesome-swift](https://github.com/matteocrippa/awesome-swift)

## 🚀 Deployment

### GitHub Pages

This project is designed to be deployed on GitHub Pages. Simply:

1. Fork this repository
2. Enable GitHub Pages in your repository settings
3. Set the source to the main branch
4. GitHub Actions will automatically update the data daily

### Local Development

To run this project locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/ultimate-collection.git
cd ultimate-collection

# If you want to update the data
python scripts/main.py

# Serve the site locally (one of the following)
python -m http.server
# OR using npm
npx serve
```

## 🛠️ How It Works

The system consists of three main components:

1. **Data Extraction**: Scripts in the `scripts/` directory clone awesome lists repositories, parse their README.md files, and extract structured data.

2. **URL Validation**: All resources are filtered to ensure they have valid URLs, improving the quality of the collection.

3. **Web Interface**: A static HTML/CSS/JS application that loads the extracted data and provides a searchable interface.

## 🔄 Automated Updates

A GitHub Actions workflow runs daily to:

1. Clone/update the source awesome list repositories
2. Extract and filter the data
3. Update the JSON data files
4. Commit and push the changes to the repository

This ensures that the collection stays up-to-date with the latest resources from all included awesome lists.

## 📁 Directory Structure

```
ultimate-collection/
├── .github/workflows/ - GitHub Actions workflow definitions
├── css/ - CSS files for styling
├── data/ - Extracted and processed data
├── js/ - JavaScript files for search and UI
├── logs/ - Log files (not checked into git)
├── scripts/ - Python scripts for data extraction and processing
└── index.html - Main entry point
```

## 🔧 Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Processing**: Python, BeautifulSoup4, Markdown
- **Search**: Fuse.js for fuzzy searching
- **Animation**: CSS animations for stars and aurora effects
- **Automation**: GitHub Actions for scheduled updates

## 📖 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- All the maintainers of the awesome lists included in this collection
- [sindresorhus](https://github.com/sindresorhus) for starting the awesome list movement
- [Bootstrap](https://getbootstrap.com/) for the responsive framework
- [Font Awesome](https://fontawesome.com/) for the icons
- [Fuse.js](https://fusejs.io/) for fuzzy search capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
