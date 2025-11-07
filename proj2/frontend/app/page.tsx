// app/page.tsx

export default function Home() {
  return (
    <section className="mt-16 grid place-items-center">
      <div className="w-full max-w-4xl text-center px-4">
        <h1 className="text-4xl font-bold mb-6">Welcome to Movie Munchers</h1>
        <p className="text-lg text-gray-600 mb-8">
          Snacks and a theater experience anywhere.
        </p>
        
        {/* Mission Statement */}
        <div className="bg-gray-50 rounded-xl p-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-900">Our Mission</h2>
          <p className="text-gray-700 leading-relaxed max-w-3xl mx-auto">
            Movie Munchers makes movie nights easier and more enjoyable by letting you order food directly to your theater seat. 
            The app connects local restaurants, theaters, and communities to offer convenient ordering and 
            group-booking features. A portion of every order supports non-profits, turning simple snacking into a fun 
            and socially positive experience.
          </p>
        </div>
      </div>
    </section>
  );
}
