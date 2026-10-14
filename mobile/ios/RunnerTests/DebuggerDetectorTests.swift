import XCTest
@testable import Runner

final class DebuggerDetectorTests: XCTestCase {

    var detector: DebuggerDetector!

    override func setUp() {
        super.setUp()
        detector = DebuggerDetector()
    }

    override func tearDown() {
        detector = nil
        super.tearDown()
    }

    func testDebuggerDetectorInitialization() {
        XCTAssertNotNil(detector)
    }

    func testCheckSysctlPTraced_ExecutesSuccessfully() {
        let isAttached = detector.checkSysctlPTraced()
        XCTAssertNotNil(isAttached)
    }
}
