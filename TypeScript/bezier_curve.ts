function comb(n: number, k: number): number {
    // Calculate the binomial coefficient (n choose k)
    if (k > n) return 0;
    let res = 1;
    for (let i = 0; i < k; i++) {
        res *= (n - i) / (i + 1);
    }
    return res;
}

function bezierCurve(points: number[][], numFrames: number): [number[], number[]] {
    const n = points.length - 1;
    const t_vals = Array.from({ length: numFrames }, (_, i) => Math.pow(i / (numFrames - 1), 1.5));
    const curveX: number[] = new Array(numFrames).fill(0);
    const curveY: number[] = new Array(numFrames).fill(0);

    for (let i = 0; i <= n; i++) {
        const binomialCoeff = comb(n, i);
        for (let j = 0; j < numFrames; j++) {
            const basis = binomialCoeff * Math.pow(1 - t_vals[j], n - i) * Math.pow(t_vals[j], i);
            curveX[j] += basis * points[i][0];
            curveY[j] += basis * points[i][1];
        }
    }

    return [curveX, curveY];
}

function generateStretchedCurve(
    start: [number, number],
    end: [number, number],
    numFrames: number,
    curveFactor: number = 0.5
): { Xframes: number[], Yframes: number[] } {
    const [x0, y0] = start;
    const [x1, y1] = end;

    // x offset
    let offsetX = Math.sign(x1 - x0) * Math.abs(x1 - x0) * curveFactor;
    if (x0 === x1) {
        offsetX = -Math.abs(y1 - y0) * curveFactor; // y offset
    }

    // offset control point
    const controlX = (x0 + x1) / 2 + offsetX;
    const controlY = Math.max(y0, y1) + curveFactor * Math.abs(x1 - x0) + Math.abs(y1 - y0) / 2;

    // 3 control points
    const bezierPoints = [
        [x0, y0], // start point
        [controlX, controlY], // control point
        [x1, y1]  // end point
    ];
    const [Xframes, Yframes] = bezierCurve(bezierPoints, numFrames);

    return { Xframes, Yframes };
}

const testCases: Array<[[number, number], [number, number], number, number]> = [
    [[0, 0], [5, 5], 60, 0.5],
    [[5, 0], [0, 5], 60, 0.5],  
    [[2, 0], [2, 5], 60, 0.5],   
];

test
testCases.forEach(([start, end, frames, factor]) => {
    const { Xframes, Yframes } = generateStretchedCurve(start, end, frames, factor);
    console.log(`Start: ${start} → End: ${end}`);
    console.log("Xframes:", Xframes);
    console.log("Yframes:", Yframes);
});
