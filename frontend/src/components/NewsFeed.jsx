import React, { useEffect, useState } from 'react';
import { fetchArticles, triggerIngestion } from '../services/api';
import { RefreshCw, Search, Tag, ExternalLink, Calendar } from 'lucide-react';

const COMPANIES = ["Microsoft", "Google", "Apple", "Meta"];

const NewsFeed = () => {
    const [articles, setArticles] = useState([]);
    const [selectedCompany, setSelectedCompany] = useState(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    const loadNews = async () => {
        setLoading(true);
        const data = await fetchArticles(selectedCompany);
        setArticles(data);
        setLoading(false);
    };

    const handleRefresh = async () => {
        setRefreshing(true);
        await triggerIngestion();
        // Wait a bit for ingestion to process some items
        setTimeout(async () => {
            await loadNews();
            setRefreshing(false);
        }, 5000);
    };

    useEffect(() => {
        loadNews();
    }, [selectedCompany]);

    // Grouping logic (optional, but let's just list with filters as primary view)

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-6 transition-colors duration-300">
            <div className="max-w-7xl mx-auto">
                <header className="mb-8 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div>
                        <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                            Financial Pulse
                        </h1>
                        <p className="text-slate-500 dark:text-slate-400 mt-2">
                            Real-time market intelligence for Big Tech.
                        </p>
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            onClick={handleRefresh}
                            className={`flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all ${refreshing ? 'opacity-70 cursor-not-allowed' : ''}`}
                            disabled={refreshing}
                        >
                            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
                            {refreshing ? 'Syncing...' : 'Sync News'}
                        </button>
                    </div>
                </header>

                {/* Filters */}
                <div className="flex flex-wrap gap-3 mb-8">
                    <button
                        onClick={() => setSelectedCompany(null)}
                        className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${selectedCompany === null
                            ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-md'
                            : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700'
                            }`}
                    >
                        All Companies
                    </button>
                    {COMPANIES.map(c => (
                        <button
                            key={c}
                            onClick={() => setSelectedCompany(c)}
                            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${selectedCompany === c
                                ? 'bg-blue-600 text-white shadow-md'
                                : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-blue-50 dark:hover:bg-slate-700'
                                }`}
                        >
                            {c}
                        </button>
                    ))}
                </div>

                {/* Grid */}
                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
                        {[1, 2, 3, 4, 5, 6].map(i => (
                            <div key={i} className="h-64 bg-white dark:bg-slate-800 rounded-xl shadow-sm"></div>
                        ))}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {articles.map((article) => (
                            <article
                                key={article.id}
                                className="group bg-white dark:bg-slate-800 rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-100 dark:border-slate-700 overflow-hidden flex flex-col"
                            >
                                <div className="p-6 flex-grow">
                                    <div className="flex items-center gap-2 mb-3">
                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                                            {article.company}
                                        </span>
                                        <span className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-1">
                                            <Calendar className="w-3 h-3" />
                                            {new Date(article.published_at).toLocaleDateString()}
                                        </span>
                                    </div>

                                    <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                                        <a href={article.url} target="_blank" rel="noreferrer">
                                            {article.title}
                                        </a>
                                    </h3>

                                    <div className="text-sm text-slate-600 dark:text-slate-300 mb-4 bg-slate-50 dark:bg-slate-900/50 p-3 rounded-lg border-l-4 border-indigo-500">
                                        {article.summary || "No summary available."}
                                    </div>
                                </div>

                                <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-700 flex justify-end items-center">
                                    <a
                                        href={article.url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="text-indigo-600 dark:text-indigo-400 text-sm font-semibold flex items-center gap-1 hover:underline"
                                    >
                                        Read full <ExternalLink className="w-3 h-3" />
                                    </a>
                                </div>
                            </article>
                        ))}
                    </div>
                )}

                {!loading && articles.length === 0 && (
                    <div className="text-center py-20">
                        <p className="text-slate-500">No news found. Try hitting Sync News.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default NewsFeed;
