# 🌟 Soluify™ - App Ally 🌟

**Effortlessly Manage All Your Non-Docker Self-Hosted Applications with a Single Command**

![app-ally](https://github.com/user-attachments/assets/46956e73-0d1b-40e8-afbd-6bda6a1e17bf)

---

## Features 🚀

- **Easy Application Management**: Start, stop, and restart applications with simple commands.
- **Live Logs** 📜: View real-time logs for each application.
- **Batch Operations** 🔄: Start or stop all applications at once.
- **Tmux Integration** 🖥️: Manage applications in isolated tmux sessions.
- **User-Friendly CLI** 🛠️: Intuitive command-line interface with typewriter-style branding.
- **Configuration Management** 🗃️: Easily configure applications using a JSON file.
- **Gradient Branding** 🎨: Enjoy a visually appealing gradient effect in the CLI.

## Requirements 📋

To run App Ally, ensure you have the following dependencies installed:

- Python 3.6+
- `colorama` library
- `tmux` (terminal multiplexer)

You can install the required Python library using `pip`:

```bash
pip install colorama
```

## Configuration ⚙️

App Ally uses a `config.json` file to manage application configurations. Below is an example of how to structure this file:

### Example `config.json`

```json
{
    "applications": {
        "example1": {
            "start_command": "cd '/path/to/example1' && sudo npm start",
            "log_file": "/tmp/example1.log"
        },
        "example2": {
            "directory": "/path/to/example2",
            "start_command": "cd '/path/to/example2' && sudo node server/server.js",
            "log_file": "/tmp/example2.log"
        }
    }
}
```

### Explanation

- **example1**: An example application with a start command that changes the directory and starts the application using `npm start`. Logs are stored in `/tmp/example1.log`.
- **example2**: Another example application with a specified directory and a start command that uses `node` to start a server. Logs are stored in `/tmp/example2.log`.

## Usage 💻

### Starting the Application

To start the App Ally, simply run:

```bash
python app_ally.py
```

### Available Commands

![image](https://github.com/user-attachments/assets/89abbc14-5244-47ab-9e93-a9a208607b74)

### Example Commands

- Start an application:

  ```bash
  start example1
  ```

- Stop an application:

  ```bash
  stop example1
  ```

- View logs of an application:

  ```bash
  view example1
  ```

- List all applications:

  ```bash
  list
  ```

- Add a new application:

  ```bash
  add
  ```

- Remove an application:

  ```bash
  remove example1
  ```

## Possible Feature Roadmap 🛤️

Here are some potential features App Ally could use:

1. 🔲**Web Interface** 🌐: A web-based dashboard to manage applications.
2. 🔲**Notification System** 🔔: Email or SMS notifications for application status changes.
3. 🔲**Advanced Logging** 📊: Enhanced logging capabilities with filtering and searching.
4. 🔲**User Roles and Permissions** 🔐: Role-based access control for managing applications.
5. 🔲**Integration with CI/CD** 🔄: Seamless integration with CI/CD pipelines for automated deployments.
6. 🔲**Resource Monitoring** 📈: Monitor resource usage (CPU, memory) for each application.
7. 🔲**Backup and Restore** 💾: Automated backup and restore functionality for application data.

## Contributing 🤝

We welcome contributions from the community. If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request on our [GitHub repository](https://github.com/Woahai321/App-Ally).

## License 📜

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contact 📧

For any inquiries or support, please contact [Soluify™](https://soluify.com/contact/).

---

By using App Ally, you agree to the terms and conditions outlined by Soluify™. Happy managing!

---

**GitHub Repository Structure**

```
App-Ally/
├── app_ally.py
├── config.json
├── README.md
└── LICENSE
```

## License

```text
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/
```

---

By following these instructions, you can easily set up and manage your self-hosted applications using App Ally. For more information and updates, visit our [GitHub repository](https://github.com/Woahai321/App-Ally) or contact us @ [Soluify™](https://soluify.com/contact/).
