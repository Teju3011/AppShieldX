import XCTest
@testable import Runner

final class JailbreakDetectorTests: XCTestCase {

    var detector: JailbreakDetector!

    override func setUp() {
        super.setUp()
        detector = JailbreakDetector()
    }

    override func tearDown() {
        detector = nil
        super.tearDown()
    }

    func testDetectorInitialization() {
        XCTAssertNotNil(detector)
    }

    func testCheckFilesystemPaths_DoesNotThrow() {
        let detected = detector.checkFilesystemPaths()
        // In a sandboxed test environment without jailbreak apps, returns false
        XCTAssertFalse(detected)
    }

    func testCheckSandboxEscape_StandardSandboxFailsWrite() {
        let escaped = detector.checkSandboxEscape()
        // Sandboxed app should be forbidden from writing to /private/
        XCTAssertFalse(escaped)
    }
}
