import UIKit
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {

    private var privacyBlurView: UIVisualEffectView?

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        GeneratedPluginRegistrant.register(with: self)

        // Register Native Security MethodChannel
        if let controller = window?.rootViewController as? FlutterViewController {
            let channel = FlutterMethodChannel(
                name: RuntimeProtectionMethodChannelHandler.channelName,
                binaryMessenger: controller.binaryMessenger
            )
            let handler = RuntimeProtectionMethodChannelHandler()
            channel.setMethodCallHandler { (call, result) in
                handler.handle(call, result: result)
            }
        }

        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    // MARK: - Background Privacy Protection (Thumbnail Masking)

    override func applicationWillResignActive(_ application: UIApplication) {
        super.applicationWillResignActive(application)
        applyPrivacyProtection()
    }

    override func applicationDidBecomeActive(_ application: UIApplication) {
        super.applicationDidBecomeActive(application)
        removePrivacyProtection()
    }

    private func applyPrivacyProtection() {
        guard privacyBlurView == nil, let window = self.window else { return }
        let blurEffect = UIBlurEffect(style: .dark)
        let blurView = UIVisualEffectView(effect: blurEffect)
        blurView.frame = window.bounds
        blurView.tag = 9999
        window.addSubview(blurView)
        self.privacyBlurView = blurView
    }

    private func removePrivacyProtection() {
        privacyBlurView?.removeFromSuperview()
        privacyBlurView = nil
    }
}
