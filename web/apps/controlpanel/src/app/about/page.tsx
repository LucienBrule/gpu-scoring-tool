
import { Card } from "@repo/ui/card";
import { Button } from "@repo/ui/button";

export default function AboutPage() {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4">
            <div className="max-w-4xl mx-auto">
                {/* Hero Section */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">
                        About Us
                    </h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        We're passionate about building exceptional digital experiences
                        that make a difference in people's lives.
                    </p>
                </div>

                {/* Main Content Cards */}
                <div className="grid md:grid-cols-2 gap-8 mb-12">
                    <Card className="p-8">
                        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                            Our Mission
                        </h2>
                        <p className="text-gray-600 leading-relaxed">
                            To create innovative solutions that empower businesses and
                            individuals to achieve their goals through cutting-edge
                            technology and thoughtful design.
                        </p>
                    </Card>

                    <Card className="p-8">
                        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                            Our Vision
                        </h2>
                        <p className="text-gray-600 leading-relaxed">
                            A world where technology seamlessly integrates into daily life,
                            making complex tasks simple and enabling everyone to focus on
                            what truly matters.
                        </p>
                    </Card>
                </div>

                {/* Values Section */}
                <Card className="p-8 mb-12">
                    <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
                        Our Values
                    </h2>
                    <div className="grid md:grid-cols-3 gap-6">
                        <div className="text-center">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                Innovation
                            </h3>
                            <p className="text-gray-600 text-sm">
                                Constantly pushing boundaries to deliver breakthrough solutions
                            </p>
                        </div>
                        <div className="text-center">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                Quality
                            </h3>
                            <p className="text-gray-600 text-sm">
                                Committed to excellence in every detail of our work
                            </p>
                        </div>
                        <div className="text-center">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                Collaboration
                            </h3>
                            <p className="text-gray-600 text-sm">
                                Building strong partnerships with our clients and community
                            </p>
                        </div>
                    </div>
                </Card>

                {/* Call to Action */}
                <div className="text-center">
                    <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                        Ready to Work Together?
                    </h2>
                    <p className="text-gray-600 mb-6">
                        Let's discuss how we can help bring your vision to life.
                    </p>
                    <div className="space-x-4">
                        <Button variant="default" size="lg">
                            Get in Touch
                        </Button>
                        <Button variant="outline" size="lg">
                            View Our Work
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}