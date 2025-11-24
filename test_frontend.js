// Add this to your browser console to test the addMessage function
// with mock sources containing clickable links

// Mock sources data
const mockSources = [
    {
        text: "Building Towards Computer Use - Lesson 3",
        link: "https://learn.deeplearning.ai/courses/building-toward-computer-use-with-anthropic/lesson/zrgb6/multimodal-requests"
    },
    {
        text: "MCP Course - Lesson 1", 
        link: "https://learn.deeplearning.ai/courses/building-toward-computer-use-with-anthropic/lesson/gi7jq/overview"
    },
    "Some Course - No Link Available"
];

// Test the addMessage function
addMessage("This is a test response with clickable source links.", "assistant", mockSources);