
class NotificationController {
  static instance;

  static getInstance() {
    if (!NotificationController.instance) {
      NotificationController.instance = new NotificationController();
    }
    return NotificationController.instance;
  }

  showError(message) {
    console.log(message)
  }
}

export default NotificationController