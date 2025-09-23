
use criterion::{criterion_group, criterion_main, Criterion};
use pt_core::compact::kk_winding_mass2;

fn bench_kk(c: &mut Criterion) {
    c.bench_function("kk_winding_mass2 grid", |b| {
        b.iter(|| {
            let mut acc = 0.0;
            for m1 in -10..=10 {
                for m2 in -10..=10 {
                    for w1 in -5..=5 {
                        for w2 in -5..=5 {
                            acc += kk_winding_mass2(m1,m2,w1,w2,1.2,0.9,1.0);
                        }
                    }
                }
            }
            acc
        })
    });
}

criterion_group!(benches, bench_kk);
criterion_main!(benches);
