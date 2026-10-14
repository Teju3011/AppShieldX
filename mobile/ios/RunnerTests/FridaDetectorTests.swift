import XCTest
@testable import Runner

final class FridaDetectorTests: XCTestCase {

    var detector: FridaDetector!

    override func setUp() {
        super.setUp()
        detector = FridaDetector()
    }

    override func tearDown() {
        detector = nil
        super.tearDown()
    }

    func testFridaDetectorInitialization() {
        XCTAssertNotNil(detector)
    }

    func testCheckDyldImages_DoesNotCrash() {
        let detected = detector.checkDyldImages()
        XCTAssertFalse(detected)
    }

    func testCheckFridaSymbols_DoesNotCrash() {
        let detected = detector.checkFridaSymbols()
        XCTAssertFalse(detected)
    }
}
