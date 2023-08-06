# Copyright 2019 DeepMind Technologies Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Unit tests for `distributions.py`."""

from absl.testing import absltest
from absl.testing import parameterized
import chex
import jax
import numpy as np
from rlax._src import distributions


class CategoricalSampleTest(parameterized.TestCase):

  @chex.all_variants()
  def test_categorical_sample(self):
    key = np.array([1, 2], dtype=np.uint32)
    probs = np.array([0.2, 0.3, 0.5])
    sample = self.variant(distributions.categorical_sample)(key, probs)
    self.assertEqual(sample, 0)

  @chex.all_variants()
  @parameterized.parameters(
      ((-1., 10., -1.),),
      ((0., 0., 0.),),
      ((1., np.inf, 3.),),
      ((1., 2., -np.inf),),
      ((1., 2., np.nan),),
  )
  def test_categorical_sample_on_invalid_distributions(self, probs):
    key = np.array([1, 2], dtype=np.uint32)
    probs = np.asarray(probs)
    sample = self.variant(distributions.categorical_sample)(key, probs)
    self.assertEqual(sample, -1)


class SoftmaxTest(parameterized.TestCase):

  def setUp(self):
    super(SoftmaxTest, self).setUp()

    self.logits = np.array([[1, 1, 0], [1, 2, 0]], dtype=np.float32)
    self.samples = np.array([0, 1], dtype=np.int32)

    self.expected_probs = np.array(  # softmax with temperature=10
        [[0.34425336, 0.34425336, 0.31149334],
         [0.332225, 0.3671654, 0.3006096]],
        dtype=np.float32)
    probs = np.array(  # softmax with temperature=1
        [[0.42231882, 0.42231882, 0.15536241],
         [0.24472848, 0.66524094, 0.09003057]],
        dtype=np.float32)
    logprobs = np.log(probs)
    self.expected_logprobs = np.array(
        [logprobs[0][self.samples[0]], logprobs[1][self.samples[1]]])
    self.expected_entropy = -np.sum(probs * logprobs, axis=-1)

  @chex.all_variants()
  def test_softmax_probs(self):
    """Tests for a single element."""
    distrib = distributions.softmax(temperature=10.)
    softmax = self.variant(distrib.probs)
    # For each element in the batch.
    for logits, expected in zip(self.logits, self.expected_probs):
      # Test outputs.
      actual = softmax(logits)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_softmax_probs_batch(self):
    """Tests for a full batch."""
    distrib = distributions.softmax(temperature=10.)
    softmax = self.variant(distrib.probs)
    # Test softmax output in batch.
    actual = softmax(self.logits)
    np.testing.assert_allclose(self.expected_probs, actual, atol=1e-4)

  @chex.all_variants()
  def test_softmax_logprob(self):
    """Tests for a single element."""
    distrib = distributions.softmax()
    logprob_fn = self.variant(distrib.logprob)
    # For each element in the batch.
    for logits, samples, expected in zip(
        self.logits, self.samples, self.expected_logprobs):
      # Test output.
      actual = logprob_fn(samples, logits)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_softmax_logprob_batch(self):
    """Tests for a full batch."""
    distrib = distributions.softmax()
    logprob_fn = self.variant(distrib.logprob)
    # Test softmax output in batch.
    actual = logprob_fn(self.samples, self.logits)
    np.testing.assert_allclose(self.expected_logprobs, actual, atol=1e-4)

  @chex.all_variants()
  def test_softmax_entropy(self):
    """Tests for a single element."""
    distrib = distributions.softmax()
    entropy_fn = self.variant(distrib.entropy)
    # For each element in the batch.
    for logits, expected in zip(self.logits, self.expected_entropy):
      # Test outputs.
      actual = entropy_fn(logits)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_softmax_entropy_batch(self):
    """Tests for a full batch."""
    distrib = distributions.softmax()
    entropy_fn = self.variant(distrib.entropy)
    # Test softmax output in batch.
    actual = entropy_fn(self.logits)
    np.testing.assert_allclose(self.expected_entropy, actual, atol=1e-4)


class EpsilonSoftmaxTest(parameterized.TestCase):

  def setUp(self):
    super(EpsilonSoftmaxTest, self).setUp()

    self.logits = np.array([[1, 1, 0], [1, 2, 0]], dtype=np.float32)
    self.samples = np.array([0, 1], dtype=np.int32)

    self.expected_probs = np.array(  # softmax with temperature=10
        [[0.34316134, 0.34316134, 0.3136773],
         [0.3323358, 0.36378217, 0.30388197]],
        dtype=np.float32)
    probs = np.array(  # softmax with temperature=10
        [[0.34316134, 0.34316134, 0.3136773],
         [0.3323358, 0.36378217, 0.30388197]],
        dtype=np.float32)
    probs = distributions._mix_with_uniform(probs, epsilon=0.1)
    logprobs = np.log(probs)
    self.expected_logprobs = np.array(
        [logprobs[0][self.samples[0]], logprobs[1][self.samples[1]]])
    self.expected_entropy = -np.sum(probs * logprobs, axis=-1)

  @chex.all_variants()
  def test_softmax_probs(self):
    """Tests for a single element."""
    distrib = distributions.epsilon_softmax(epsilon=0.1,
                                            temperature=10.)
    softmax = self.variant(distrib.probs)
    # For each element in the batch.
    for logits, expected in zip(self.logits, self.expected_probs):
      # Test outputs.
      actual = softmax(logits)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_softmax_probs_batch(self):
    """Tests for a full batch."""
    distrib = distributions.epsilon_softmax(epsilon=0.1,
                                            temperature=10.)
    softmax = self.variant(distrib.probs)
    # Test softmax output in batch.
    actual = softmax(self.logits)
    np.testing.assert_allclose(self.expected_probs, actual, atol=1e-4)

  @chex.all_variants()
  def test_safe_epsilon_softmax_equivalence(self):
    distrib = distributions.safe_epsilon_softmax(epsilon=0.1,
                                                 temperature=10.)
    softmax = self.variant(distrib.probs)
    # Test softmax output in batch.
    actual = softmax(self.logits)
    np.testing.assert_allclose(self.expected_probs, actual, atol=1e-4)


class GreedyTest(parameterized.TestCase):

  def setUp(self):
    super(GreedyTest, self).setUp()

    self.preferences = np.array([[1, 1, 0], [1, 2, 0]], dtype=np.float32)
    self.samples = np.array([0, 1], dtype=np.int32)

    self.expected_probs = np.array(
        [[0.5, 0.5, 0.], [0., 1., 0.]], dtype=np.float32)
    self.expected_logprob = np.array(
        [-0.6931472, 0.], dtype=np.float32)
    self.expected_entropy = np.array(
        [0.6931472, 0.], dtype=np.float32)

  @chex.all_variants()
  def test_greedy_probs(self):
    """Tests for a single element."""
    distrib = distributions.greedy()
    greedy = self.variant(distrib.probs)
    # For each element in the batch.
    for preferences, expected in zip(self.preferences, self.expected_probs):
      # Test outputs.
      actual = greedy(preferences)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_probs_batch(self):
    """Tests for a full batch."""
    distrib = distributions.greedy()
    greedy = self.variant(distrib.probs)
    # Test greedy output in batch.
    actual = greedy(self.preferences)
    np.testing.assert_allclose(self.expected_probs, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_logprob(self):
    """Tests for a single element."""
    distrib = distributions.greedy()
    logprob_fn = self.variant(distrib.logprob)
    # For each element in the batch.
    for preferences, samples, expected in zip(
        self.preferences, self.samples, self.expected_logprob):
      # Test output.
      actual = logprob_fn(samples, preferences)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_logprob_batch(self):
    """Tests for a full batch."""
    distrib = distributions.greedy()
    logprob_fn = self.variant(distrib.logprob)
    # Test greedy output in batch.
    actual = logprob_fn(self.samples, self.preferences)
    np.testing.assert_allclose(self.expected_logprob, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_entropy(self):
    """Tests for a single element."""
    distrib = distributions.greedy()
    entropy_fn = self.variant(distrib.entropy)
    # For each element in the batch.
    for preferences, expected in zip(self.preferences, self.expected_entropy):
      # Test outputs.
      actual = entropy_fn(preferences)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_entropy_batch(self):
    """Tests for a full batch."""
    distrib = distributions.greedy()
    entropy_fn = self.variant(distrib.entropy)
    # Test greedy output in batch.
    actual = entropy_fn(self.preferences)
    np.testing.assert_allclose(self.expected_entropy, actual, atol=1e-4)


class EpsilonGreedyTest(parameterized.TestCase):

  def setUp(self):
    super(EpsilonGreedyTest, self).setUp()
    self.epsilon = 0.2

    self.preferences = np.array([[1, 1, 0, 0], [1, 2, 0, 0]], dtype=np.float32)
    self.samples = np.array([0, 1], dtype=np.int32)

    self.expected_probs = np.array(
        [[0.45, 0.45, 0.05, 0.05], [0.05, 0.85, 0.05, 0.05]], dtype=np.float32)
    self.expected_logprob = np.array(
        [-0.7985077, -0.1625189], dtype=np.float32)
    self.expected_entropy = np.array(
        [1.01823008, 0.58750093], dtype=np.float32)

  @chex.all_variants()
  def test_greedy_probs(self):
    """Tests for a single element."""
    distrib = distributions.epsilon_greedy(self.epsilon)
    probs_fn = self.variant(distrib.probs)
    # For each element in the batch.
    for preferences, expected in zip(self.preferences, self.expected_probs):
      # Test outputs.
      actual = probs_fn(preferences)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_probs_batch(self):
    """Tests for a full batch."""
    distrib = distributions.epsilon_greedy(self.epsilon)
    probs_fn = self.variant(distrib.probs)
    # Test greedy output in batch.
    actual = probs_fn(self.preferences)
    np.testing.assert_allclose(self.expected_probs, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_logprob(self):
    """Tests for a single element."""
    distrib = distributions.epsilon_greedy(self.epsilon)
    logprob_fn = self.variant(distrib.logprob)
    # For each element in the batch.
    for preferences, samples, expected in zip(
        self.preferences, self.samples, self.expected_logprob):
      # Test output.
      actual = logprob_fn(samples, preferences)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_logprob_batch(self):
    """Tests for a full batch."""
    distrib = distributions.epsilon_greedy(self.epsilon)
    logprob_fn = self.variant(distrib.logprob)
    # Test greedy output in batch.
    actual = logprob_fn(self.samples, self.preferences)
    np.testing.assert_allclose(self.expected_logprob, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_entropy(self):
    """Tests for a single element."""
    distrib = distributions.epsilon_greedy(self.epsilon)
    entropy_fn = self.variant(distrib.entropy)
    # For each element in the batch.
    for preferences, expected in zip(self.preferences, self.expected_entropy):
      # Test outputs.
      actual = entropy_fn(preferences)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_greedy_entropy_batch(self):
    """Tests for a full batch."""
    distrib = distributions.epsilon_greedy(self.epsilon)
    entropy_fn = self.variant(distrib.entropy)
    # Test greedy output in batch.
    actual = entropy_fn(self.preferences)
    np.testing.assert_allclose(self.expected_entropy, actual, atol=1e-4)

  @chex.all_variants()
  def test_safe_epsilon_softmax_equivalence(self):
    distrib = distributions.safe_epsilon_softmax(epsilon=self.epsilon,
                                                 temperature=0)
    probs_fn = self.variant(distrib.probs)
    # Test greedy output in batch.
    actual = probs_fn(self.preferences)
    np.testing.assert_allclose(self.expected_probs, actual, atol=1e-4)

    logprob_fn = self.variant(distrib.logprob)
    # Test greedy output in batch.
    actual = logprob_fn(self.samples, self.preferences)
    np.testing.assert_allclose(self.expected_logprob, actual, atol=1e-4)

    sample_fn = self.variant(distrib.sample)
    # Optionally convert to device array.
    key = np.array([1, 2], dtype=np.uint32)
    actions = sample_fn(key, self.preferences)
    # test just the shape
    self.assertEqual(actions.shape, (2,))


class GaussianDiagonalTest(parameterized.TestCase):

  def setUp(self):
    super(GaussianDiagonalTest, self).setUp()

    self.mu = np.array([[1., -1], [0.1, -0.1]], dtype=np.float32)
    self.sigma = np.array([[0.1, 0.1], [0.2, 0.3]], dtype=np.float32)
    self.sample = np.array([[1.2, -1.1], [-0.1, 0.]], dtype=np.float32)

    # Expected values for the distribution's function were computed using
    # tfd.MultivariateNormalDiag (from the tensorflow_probability package).
    self.expected_prob_a = np.array(
        [1.3064219, 1.5219283], dtype=np.float32)
    self.expected_logprob_a = np.array(
        [0.26729202, 0.41997814], dtype=np.float32)
    self.expected_entropy = np.array(
        [-1.7672932, 0.02446628], dtype=np.float32)

  @chex.all_variants()
  def test_gaussian_prob(self):
    """Tests for a single element."""
    distrib = distributions.gaussian_diagonal()
    prob_fn = self.variant(distrib.prob)
    # For each element in the batch.
    for mu, sigma, sample, expected in zip(
        self.mu, self.sigma, self.sample, self.expected_prob_a):
      # Test outputs.
      actual = prob_fn(sample, mu, sigma)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_gaussian_prob_batch(self):
    """Tests for a full batch."""
    distrib = distributions.gaussian_diagonal()
    prob_fn = self.variant(distrib.prob)
    # Test greedy output in batch.
    actual = prob_fn(self.sample, self.mu, self.sigma)
    np.testing.assert_allclose(self.expected_prob_a, actual, atol=1e-4)

  @chex.all_variants()
  def test_gaussian_logprob(self):
    """Tests for a single element."""
    distrib = distributions.gaussian_diagonal()
    logprob_fn = self.variant(distrib.logprob)
    # For each element in the batch.
    for mu, sigma, sample, expected in zip(
        self.mu, self.sigma, self.sample, self.expected_logprob_a):
      # Test output.
      actual = logprob_fn(sample, mu, sigma)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_gaussian_logprob_batch(self):
    """Tests for a full batch."""
    distrib = distributions.gaussian_diagonal()
    logprob_fn = self.variant(distrib.logprob)
    # Test greedy output in batch.
    actual = logprob_fn(self.sample, self.mu, self.sigma)
    np.testing.assert_allclose(self.expected_logprob_a, actual, atol=1e-4)

  @chex.all_variants()
  def test_gaussian_entropy(self):
    """Tests for a single element."""
    distrib = distributions.gaussian_diagonal()
    entropy_fn = self.variant(distrib.entropy)
    # For each element in the batch.
    for mu, sigma, expected in zip(
        self.mu, self.sigma, self.expected_entropy):
      # Test outputs.
      actual = entropy_fn(mu, sigma)
      np.testing.assert_allclose(expected, actual, atol=1e-4)

  @chex.all_variants()
  def test_gaussian_entropy_batch(self):
    """Tests for a full batch."""
    distrib = distributions.gaussian_diagonal()
    entropy_fn = self.variant(distrib.entropy)
    # Test greedy output in batch.
    actual = entropy_fn(self.mu, self.sigma)
    np.testing.assert_allclose(self.expected_entropy, actual, atol=1e-4)


class ImportanceSamplingTest(parameterized.TestCase):

  def setUp(self):
    super(ImportanceSamplingTest, self).setUp()

    self.pi_logits = np.array([[0.2, 0.8], [0.6, 0.4]], dtype=np.float32)
    self.mu_logits = np.array([[0.8, 0.2], [0.6, 0.4]], dtype=np.float32)
    self.actions = np.array([1, 0], dtype=np.int32)

    pi = jax.nn.softmax(self.pi_logits)
    mu = jax.nn.softmax(self.mu_logits)
    self.expected_rhos = np.array(
        [pi[0][1] / mu[0][1], pi[1][0] / mu[1][0]], dtype=np.float32)

  @chex.all_variants()
  def test_importance_sampling_ratios_batch(self):
    """Tests for a full batch."""
    ratios_fn = self.variant(
        distributions.categorical_importance_sampling_ratios)
    # Test softmax output in batch.
    actual = ratios_fn(self.pi_logits, self.mu_logits, self.actions)
    np.testing.assert_allclose(self.expected_rhos, actual, atol=1e-4)


class CategoricalKLTest(parameterized.TestCase):

  def setUp(self):
    super(CategoricalKLTest, self).setUp()
    self.p_logits = np.array([[1, 1, 0], [1, 2, 0]], dtype=np.float32)
    p_probs = np.array([[0.42231882, 0.42231882, 0.15536241],
                        [0.24472848, 0.66524094, 0.09003057]],
                       dtype=np.float32)
    p_logprobs = np.log(p_probs)
    self.q_logits = np.array([[1, 2, 0], [1, 1, 0]], dtype=np.float32)
    q_probs = np.array([[0.24472848, 0.66524094, 0.09003057],
                        [0.42231882, 0.42231882, 0.15536241]],
                       dtype=np.float32)
    q_logprobs = np.log(q_probs)

    self.expected_kl = np.sum(p_probs * (p_logprobs - q_logprobs), axis=-1)

  @chex.all_variants()
  def test_categorical_kl_divergence_batch(self):
    """Tests for a full batch."""
    kl_fn = self.variant(distributions.categorical_kl_divergence)
    # Test softmax output in batch.
    actual = kl_fn(self.p_logits, self.q_logits)
    np.testing.assert_allclose(self.expected_kl, actual, atol=1e-4)


class CategoricalCrossEntropyTest(parameterized.TestCase):

  def setUp(self):
    super(CategoricalCrossEntropyTest, self).setUp()

    self.labels = np.array([[0., 1., 0.], [1., 0., 0.]], dtype=np.float32)
    self.logits = np.array([[10., 1., -2.], [1., 4., 0.2]], dtype=np.float32)

    self.expected = np.array([9.00013, 3.0696733], dtype=np.float32)

  @chex.all_variants()
  def test_categorical_cross_entropy_batch(self):
    """Tests for a full batch."""
    cross_entropy = self.variant(jax.vmap(
        distributions.categorical_cross_entropy))
    # Test outputs.
    actual = cross_entropy(self.labels, self.logits)
    np.testing.assert_allclose(self.expected, actual, atol=1e-4)


if __name__ == '__main__':
  jax.config.update('jax_numpy_rank_promotion', 'raise')
  absltest.main()
