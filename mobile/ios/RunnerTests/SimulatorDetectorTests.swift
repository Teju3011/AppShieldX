import XCTest
@testable import Runner

final class SimulatorDetectorTests: XCTestCase {

    var detector: SimulatorDetector!

    override func setUp() {
        super.setUp()
        detector = SimulatorDetector()
    }

    override func tearDown() {
        detector = nil
        super.tearDown()
    }

    func testSimulatorDetectorInitialization() {
        XCTAssertNotNil(detector)
    }

    func testIsSimulator_ExecutionIntegrity() {
        let isSim = detector.isSimulator()
        // Method executes deterministically without crashing
        XCTAssertNotNil(isSim)
    }
}
